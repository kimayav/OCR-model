import cv2
import easyocr
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from threading import Thread

class ImageProcessorApp:
    def __init__(self, root):
        self.reader = easyocr.Reader(['en'])
        self.selected_images = []

        self.root = root
        self.root.title("Select and Process Images")

        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack(padx=10, pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(padx=10, pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Images", command=self.add_images)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(self.button_frame, text="Remove Selected", command=self.remove_images)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.process_button = tk.Button(self.button_frame, text="Process Images", command=self.process_images)
        self.process_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(root, text="Save Output", command=self.save_output)
        self.save_button.pack(pady=5)

        self.text_output_frame = tk.Frame(root)
        self.text_output_frame.pack(padx=10, pady=10)

        self.text_outputs = [tk.Text(self.text_output_frame, width=50, height=10) for _ in range(6)]
        for i, text_output in enumerate(self.text_outputs):
            text_output.grid(row=i//3, column=i % 3, padx=10, pady=10)

    def add_images(self):
        file_paths = filedialog.askopenfilenames(title="Select up to 6 image files",
                                                 filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")),
                                                 multiple=True)
        if len(file_paths) > 6:
            messagebox.showwarning("Warning", "Please select up to 6 images only.")
            return

        self.selected_images.clear()
        self.selected_images.extend(file_paths)
        self.update_listbox()
        self.process_images()

    def remove_images(self):
        selected_indices = self.listbox.curselection()
        for index in selected_indices[::-1]:
            del self.selected_images[index]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for image_path in self.selected_images:
            self.listbox.insert(tk.END, image_path)

    def process_images(self):
        if len(self.selected_images) > 6:
            messagebox.showwarning("Warning", "Only the first 6 images will be processed.")
            selected_to_process = self.selected_images[:6]
        else:
            selected_to_process = self.selected_images

        for i, image_path in enumerate(selected_to_process):
            self.text_outputs[i].delete("1.0", tk.END)
            thread = Thread(target=self.process_img, args=(image_path, i))
            thread.start()

    def process_img(self, image_path, index):
        image = cv2.imread(image_path)
        if image is None:
            messagebox.showerror("Error", f"Failed to load image: {image_path}")
            return

        regions = [
            {"name": "Company Name", "coords": (115, 150, 266, 178)},
            {"name": "BILL Number", "coords": (839, 179, 975, 199)},
            {"name": "DATE", "coords": (841, 201, 973, 219)},
            {"name": "GST-IN:", "coords": (111, 241, 303, 262)},
            {"name": "Total amount", "coords": (200, 747, 265, 765)}
        ]

        offset = 5
        base_path, filename = os.path.split(image_path)
        filename_without_ext, _ = os.path.splitext(filename)

        if not os.path.exists("processed_images"):
            os.makedirs("processed_images")

        for region in regions:
            name = region["name"]
            x1, y1, x2, y2 = region["coords"]
            x1, y1, x2, y2 = x1 - offset, y1 - offset, x2 + offset, y2 + offset
            cropped_image = image[y1:y2, x1:x2]
            cropped_image_path = f'processed_images/{filename_without_ext}_cropped_{name}.jpg'
            cv2.imwrite(cropped_image_path, cropped_image)
            self.process_image(cropped_image_path, index)

    def process_image(self, image_path, index):
        image = cv2.imread(image_path)
        if image is None:
            self.insert_text(image_path, f"Failed to load image: {image_path}\n", index)
            return

        result = self.reader.readtext(image)
        text = "\n".join([detection[1] for detection in result])
        self.insert_text(image_path, text, index)

    def insert_text(self, image_path, text, index):
        self.text_outputs[index].insert(tk.END, f"Image: {image_path}\n")
        self.text_outputs[index].insert(tk.END, text + "\n\n")

    def save_output(self):
        output_texts = [text_output.get("1.0", tk.END) for text_output in self.text_outputs]
        with open("output.txt", "w") as file:
            for i, output_text in enumerate(output_texts):
                file.write(f"Output for Image {i + 1}:\n")
                file.write(output_text)
                file.write("\n" + "=" * 40 + "\n")
        messagebox.showinfo("Save Successful", "Output saved to output.txt")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
