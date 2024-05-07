import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to process image and perform OCR


def process_image(image_path):
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

    # Process each region
    for region in regions:
        name = region["name"]
        x1, y1, x2, y2 = region["coords"]
        # Add the offset
        x1, y1, x2, y2 = x1 - offset, y1 - offset, x2 + offset, y2 + offset
        cropped_image = image[y1:y2, x1:x2]
        # Save the cropped image
        cv2.imwrite(f'cropped_{name}.jpg', cropped_image)
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
        process_image(file_path)


# Create the main tkinter window
root = tk.Tk()
root.title("Image Processing and OCR")

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

# Start the tkinter event loop
# root.destroy()
root.mainloop()

with open('C:\\kimdsyyaya\\NeoThermal\\multiple_images.py', 'r') as file:
    code = file.read()
    exec(code)
