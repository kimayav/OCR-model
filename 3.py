import tkinter as tk
from tkinter import filedialog
import cv2
import easyocr as Reader
import easyocr
import re
import PIL as ImageTk


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def extract_date(text):
    date_patterns = [
        r"\b(\d{2}-\d{2}-\d{4})\b",  # DD-MM-YYYY
        r"\b(\d{2}/\d{2}/\d{4})\b",  # DD/MM/YYYY
        r"\b(\d{4}-\d{2}-\d{2})\b",  # YYYY-MM-DD
        r"\b(\d{4}/\d{2}/\d{2})\b",  # YYYY/MM/DD
        # D-D-YY or DD-D-YY or D-DD-YY or DD-DD-YY
        r"\b(\d{1,2}-\d{1,2}-\d{2})\b"
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def extract_features(list):
    features = {
        "Company Name": None,
        "Invoice Number": None,
        "Date": None,
        "GSTIN": None,
        "Products": [],
        "Total Amount": None
    }
    for i in range(len(list)):
        if "For" in list[i]:
            match = re.search(r"For\s*([A-Za-z\s]*)$", list[i])
            if match:
                features["Company Name"] = match.group(
                    1)
        elif re.search(r"(?:Invoice|Bill) No:?\s*([A-Za-z0-9]+)$", list[i], re.MULTILINE):
            match = re.search(
                r'(Invoice| Bill)? \s*\n\s*\n(.+?)\s*\n', list[i], re.MULTILINE)
            if match:
                features["Invoice Number"] = match.group(1).strip()
        elif "GSTIN" in list[i]:
            match = re.search(
                r"(GSTIN|GST|GSTin)\s*:\s*([A-Za-z0-9]+)$", list[i])
            if match:
                features["GSTIN"] = match.group(2)
            else:
                for j in range(i+1, len(list)):
                    match = re.findall(r"([A-Za-z0-9]{15})$", list[j])
                    if match and features["GSTIN"] == None:
                        features["GSTIN"] = match[0]
        elif "TOTAL\n" in list[i]:
            match = re.search(r"\d+\.\d{2}", list[i+1])
            if match:
                features["Total Amount"] = list[i+1]
        elif re.search(r"\b[A-Z][A-Za-z\s]+\b", list[i], re.MULTILINE):
            match = re.search(r"\b[A-Z]+\b", list[i], re.MULTILINE)
            # features["Products"] = match.group()
    return features


def ocr_and_extract_features(image_path, langs=["en"], gpu=False):
    image = cv2.imread(image_path)
    reader = easyocr.Reader(langs, gpu=gpu)
    results = reader.readtext(image)
    text_list = []

    for (bbox, text, prob) in results:
        text = cleanup_text(text)
        text_list.append(text)

    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(text_list))

    list1 = text_list
    features = extract_features(list1)
    return features


def select_image():
    file_path = filedialog.askopenfilename(title="Select an image file",
                                           filetypes=(("JPEG files", "*.jpg"),
                                                      ("PNG files", "*.png"),
                                                      ("All files", "*.*")))
    if file_path:
        features = ocr_and_extract_features(file_path)
        for key, value in features.items():
            text_output.insert(tk.END, f"{key}: {value}\n")

        # display_image(file_path)


def save_text():
    # Get the edited text from the text widget
    edited_text = text_output.get("1.0", tk.END)

    # Save the edited text to a file
    with open("verified_output.txt", "w") as f:
        f.write(edited_text)

# # def display_image(image_path):
#     image = cv2.imread(image_path)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image = cv2.resize(image, (400, 400))
#     image = image.fromarray(image)
#     image = ImageTk.PhotoImage(image)
#     image_label.config(image=image)
#     image_label.image = image


# Create the main window
root = tk.Tk()
root.title("OCR and Feature Extraction")

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

save_button = tk.Button(root, text="Save", command=save_text)
save_button.pack(pady=10)


# Create a label to display the selected image
image_label = tk.Label(root)
image_label.pack(pady=10)

# Create a text widget to display the extracted features
text_output = tk.Text(root, width=50, height=20)
text_output.pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
