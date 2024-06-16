import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog, messagebox
import os

reader = easyocr.Reader(['en'])
selected_images = []


def add_images():
    folder_path = "processed_images"
    if not os.path.exists(folder_path):
        messagebox.showerror("Folder Not Found",
                             "The 'processed_images' folder does not exist.")
        return

    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)
                  if file_name.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not file_paths:
        messagebox.showinfo(
            "No Images Found", "No images found in the 'processed_images' folder.")
        return

    selected_images.extend(file_paths)
    update_listbox()
    process_images()


def remove_images():
    selected_indices = listbox.curselection()
    for index in selected_indices:
        del selected_images[index]
    update_listbox()


def update_listbox():
    listbox.delete(0, tk.END)
    for image_path in selected_images:
        listbox.insert(tk.END, image_path)


def process_images():
    text_output.delete("1.0", tk.END)
    for image_path in selected_images:
        process_image(image_path)


def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", f"Failed to load image: {image_path}")
        return

    result = reader.readtext(image)
    # text_output.insert(tk.END, f"Image: {image_path}\n")
    for detection in result:
        text = detection[1]
        text_output.insert(tk.END, text + "\n")
    text_output.insert(tk.END, "\n")


def save_output():
    output_text = text_output.get("1.0", tk.END)
    with open("output.txt", "w") as file:
        file.write(output_text)
    messagebox.showinfo("Save Successful", "Output saved to output.txt")


def process_img(image_path):
    image = cv2.imread(image_path)
    regions = [
        {"name": "Company Name", "coords": (115, 150, 266, 178)},
        {"name": "BILL Number", "coords": (839, 179, 975, 199)},
        {"name": "DATE", "coords": (841, 201, 973, 219)},
        {"name": "GST-IN:", "coords": (111, 241, 303, 262)},
        {"name": "Total amount", "coords": (200, 747, 265, 765)}
    ]

    offset = 5

    if not os.path.exists("processed_images"):
        os.makedirs("processed_images")

    for region in regions:
        name = region["name"]
        x1, y1, x2, y2 = region["coords"]
        x1, y1, x2, y2 = x1 - offset, y1 - offset, x2 + offset, y2 + offset
        cropped_image = image[y1:y2, x1:x2]
        cropped_image_path = f'processed_images/cropped_{name}.jpg'
        cv2.imwrite(cropped_image_path, cropped_image)
        selected_images.append(cropped_image_path)

    update_listbox()
    process_images()


def select_image():
    file_path = filedialog.askopenfilename(title="Select an image file",
                                           filetypes=(("JPEG files", "*.jpg"),
                                                      ("PNG files", "*.png"),
                                                      ("All files", "*.*")))
    if file_path:
        process_img(file_path)


root = tk.Tk()
root.title("Select and Process Images")
listbox = tk.Listbox(root, width=50, height=5)
listbox.pack(padx=10, pady=10)
button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, padx=10, pady=10)
add_button = tk.Button(button_frame, text="Add Images", command=add_images)
add_button.pack(pady=5, fill=tk.X)
remove_button = tk.Button(
    button_frame, text="Remove Selected", command=remove_images)
remove_button.pack(pady=5, fill=tk.X)
process_button = tk.Button(
    button_frame, text="Process Images", command=process_images)
process_button.pack(pady=5, fill=tk.X)
text_output = tk.Text(root, width=50, height=10)
text_output.pack(padx=10, pady=10)
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=5)
save_button = tk.Button(root, text="Save Output", command=save_output)
save_button.pack(pady=5)
root.mainloop()
