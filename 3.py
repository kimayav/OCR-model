import tkinter as tk
from tkinter import filedialog
import cv2
import easyocr
import re
a = 0


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


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
                features["Company Name"] = match.group(1)
            elif a == 0:
                for j in range(i, len(list)):
                    match = re.search(r"For\s*([A-Za-z\s]*)$", list[i])
                    if match:
                        features["Company Name"] = match.group(
                            1).strip().replace(" ", "")

        elif re.search(r"Invoice\s*|\s*Bill\s*No\s*:?\s*", list[i]):
            match = re.search(
                r"(?:Invoice|Bill)?\s*No\s*:?[\s:]*([A-Za-z]{2}[A-Za-z0-9/-]+)", "\n".join(list[i:len(list)]))
            if match:
                features["Invoice Number"] = match.group(1)
            elif re.search(r"Invoice\s*|\s*Bill\s*No_\s*:?\s*", list[i]):
                match = re.search(
                    r"(?:Invoice|Bill)?\s*No_\s*:?[\s:]*([A-Za-z]{2}[A-Za-z0-9/-]+)", "\n".join(list[i:len(list)]))
                if match:
                    features["Invoice Number"] = match.group(1)

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

        elif "TOTAL" in list[i]:
            match = re.search(r"\d+\.\d{2}", list[i+1])
            if match:
                features["Total Amount"] = list[i+1]

        elif a == 0:
            match = re.search(
                r"(?:Date|\bBill Date\b|\bInvoice Date\b)?\s*\b(\d{1,2}\s*[-/]\s*\d{1,2}\s*[-/]\s*\d{2,4})\b", " ".join(list[i:len(list)]))
            if match:
                features["Date"] = match.group(1)

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
        image_label.config(
            text=f"Selected Image: {file_path}\nProcessing Image...")

        text_output.delete("1.0", tk.END)
        features = ocr_and_extract_features(file_path)
        for key, value in features.items():
            text_output.insert(tk.END, f"{key}: {value}\n")
        image_label.config(
            text=f"Selected Image: {file_path}\n Expected Features: ")


def select_new_image():
    text_output.delete("1.0", tk.END)
    image_label.config(text="Selecting New Image...")
    select_image()


def save_text():
    # Get the edited text from the text widget
    edited_text = text_output.get("1.0", tk.END)

    # Save the edited text to a file
    with open("verified_output.txt", "w") as f:
        f.write(edited_text)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "File saved")


# Create the main window
root = tk.Tk()
root.title("OCR and Feature Extraction")

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

# Create a button to select a new image
new_image_button = tk.Button(
    root, text="Select New Image", command=select_new_image)
new_image_button.pack(pady=10)

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
