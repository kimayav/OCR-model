import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Global list to store selected image paths
selected_images = []

# Function to add images from the 'processed_images' folder to the listbox


def add_images():
    folder_path = "processed_images"  # Path to the 'processed_images' folder
    if not os.path.exists(folder_path):
        messagebox.showerror("Folder Not Found",
                             "The 'processed_images' folder does not exist.")
        return

    # Get all files in the folder with supported extensions
    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)
                  if file_name.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not file_paths:
        messagebox.showinfo(
            "No Images Found", "No images found in the 'processed_images' folder.")
        return

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
    if image is None:
        messagebox.showerror("Error", f"Failed to load image: {image_path}")
        return

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

# Function to process an image by cropping and performing OCR


def process_img(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Define the regions to crop with a little offset
    regions = [
        {"name": "Company Name", "coords": (115, 150, 266, 178)},
        {"name": "BILL Number", "coords": (839, 179, 975, 199)},
        {"name": "DATE", "coords": (841, 201, 973, 219)},
        {"name": "GST-IN:", "coords": (111, 241, 303, 262)},
        {"name": "Total amount", "coords": (200, 747, 265, 765)}
    ]

    # Define the offset
    offset = 5

    # Create the processed images directory if it doesn't exist
    if not os.path.exists("processed_images"):
        os.makedirs("processed_images")

    # Process each region
    for region in regions:
        name = region["name"]
        x1, y1, x2, y2 = region["coords"]
        # Add the offset
        x1, y1, x2, y2 = x1 - offset, y1 - offset, x2 + offset, y2 + offset
        cropped_image = image[y1:y2, x1:x2]
        # Save the cropped image
        cv2.imwrite(f'processed_images/cropped_{name}.jpg', cropped_image)
        # Perform OCR on the cropped image
        result = reader.readtext(cropped_image)
        print(f"Text in {name}: {result}")

        # Display the cropped images
        cv2.imshow(f'Cropped {name}', cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Function to handle file selection from tkinter


def select_image():
    file_path = filedialog.askopenfilename(title="Select an image file",
                                           filetypes=(("JPEG files", "*.jpg"),
                                                      ("PNG files", "*.png"),
                                                      ("All files", "*.*")))
    if file_path:
        process_img(file_path)


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

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=5)

# Create a button to save the output
save_button = tk.Button(root, text="Save Output", command=save_output)
save_button.pack(pady=5)

# Start the tkinter event loop
root.mainloop()
