import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog, scrolledtext
import re


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def extract_features(text):
    features = {
        "Products": [],
        "Invoice Number": None,
        "Company Name": None,
        "GST": None,
        "Total Amount": None
    }
    features["Company Name"] = text[1]

    for i in range(len(text)):
        if "Invoice No:\n" in text[i]:
            match = re.search(r"[A-Z]{2}\d{5}\n", text[i+1])
            if match:
                features["Invoice Number"] = text[i+1]
        elif "GSTIN\n" in text[i]:
            features["GST"] = text[i+1]
        elif "TOTAL\n" in text[i]:
            match = re.search(r"\d+\.\d{2}", text[i+1])
            if match:
                features["Total Amount"] = text[i+1]
        elif "Product\n" in text[i]:
            features["Products"] = str(text[i+9])

    return features


def perform_ocr(file_path):
    # Perform OCR
    image = cv2.imread(file_path)
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image)

    # Process OCR results
    text = [result[1] for result in results]
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(text))

    features = extract_features(text)

    # Display extracted features in the GUI
    output_text.delete(1.0, tk.END)
    for key, value in features.items():
        output_text.insert(tk.END, f"{key}: {value}\n")


def select_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        perform_ocr(file_path)


root = tk.Tk()
root.title("Invoice OCR")

# Create a button to select an image file
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=20)

# Create a text area to display the extracted features
output_text = scrolledtext.ScrolledText(root, width=50, height=20)
output_text.pack(padx=20, pady=10)

root.mainloop()
