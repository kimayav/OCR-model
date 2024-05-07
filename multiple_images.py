import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog, messagebox

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Global list to store selected image paths
selected_images = []

# Function to add images to the listbox


def add_images():
    file_paths = filedialog.askopenfilenames(title="Select image files",
                                             filetypes=(("JPEG files", "*.jpg"),
                                                        ("PNG files", "*.png"),
                                                        ("All files", "*.*")))
    if file_paths:
        selected_images.extend(file_paths)
        update_listbox()

# Function to remove selected images from the listbox


def remove_images():
    selected_indices = listbox.curselection()
    for index in selected_indices:
        del selected_images[index]
    update_listbox()

# Function to update the listbox with selected images


def update_listbox():
    listbox.delete(0, tk.END)
    for image_path in selected_images:
        listbox.insert(tk.END, image_path)

# Function to process all selected images


def process_images():
    for image_path in selected_images:
        process_image(image_path)

# Function to process a single image and perform OCR


def process_image(image_path):
    image = cv2.imread(image_path)
    result = reader.readtext(image)
    for detection in result:
        text = detection[1]
        text_output.insert(tk.END, text + "\n")  # Display detected text
    text_output.insert(tk.END, "\n")  # Add a newline for readability

# Function to save the detected text to a file


def save_output():
    output_text = text_output.get("1.0", tk.END)
    with open("output.txt", "w") as file:
        file.write(output_text)
    messagebox.showinfo("Save Successful", "Output saved to output.txt")


# Create the main tkinter window
root = tk.Tk()
root.title("Select and Process Images")

# Create a listbox to display selected images
listbox = tk.Listbox(root, width=50, height=5)
listbox.pack(padx=10, pady=10)

# Create a frame to contain the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create buttons to add, remove, and process images
add_button = tk.Button(button_frame, text="Add Images", command=add_images)
add_button.pack(pady=5, fill=tk.X)
remove_button = tk.Button(
    button_frame, text="Remove Selected", command=remove_images)
remove_button.pack(pady=5, fill=tk.X)
process_button = tk.Button(
    button_frame, text="Process Images", command=process_images)
process_button.pack(pady=5, fill=tk.X)

# Create a text widget to display detected text
text_output = tk.Text(root, width=50, height=10)
text_output.pack(padx=10, pady=10)

# Create a button to save the output
save_button = tk.Button(root, text="Save Output", command=save_output)
save_button.pack(pady=5)

# Start the tkinter event loop
root.mainloop()
