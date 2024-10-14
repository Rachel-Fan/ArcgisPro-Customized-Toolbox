import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class ImageViewer:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.image_folder = os.path.join(root_folder, "images")
        self.glcm_folder = os.path.join(root_folder, "glcm")
        self.filenames = sorted(os.listdir(self.image_folder))
        self.current_index = 0

        self.window = tk.Tk()
        self.window.title("Image and GLCM Viewer")

        # Left frame for original image and controls
        self.left_frame = ttk.Frame(self.window)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label_image = tk.Label(self.left_frame)
        self.label_image.pack(padx=10, pady=10)

        self.label_name_image = tk.Label(self.left_frame)
        self.label_name_image.pack()

        # Next and previous buttons
        self.button_frame = ttk.Frame(self.left_frame)
        self.button_frame.pack(padx=10, pady=10)

        self.btn_prev = ttk.Button(self.button_frame, text="Previous", command=self.show_previous_image)
        self.btn_prev.grid(row=0, column=0, padx=5)

        self.btn_next = ttk.Button(self.button_frame, text="Next", command=self.show_next_image)
        self.btn_next.grid(row=0, column=1, padx=5)

        # Right frame for GLCM images
        self.right_frame = ttk.Frame(self.window)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.glcm_images_frame = ttk.Frame(self.right_frame)
        self.glcm_images_frame.pack(padx=10, pady=10)

        self.glcm_labels = []

        self.show_current_image()

    def show_current_image(self):
        if self.filenames:
            filename = self.filenames[self.current_index]
            image_path = os.path.join(self.image_folder, filename)

            try:
                with Image.open(image_path) as img:
                    # Display original image
                    img.thumbnail((600, 600))
                    photo_img = ImageTk.PhotoImage(img)
                    self.label_image.config(image=photo_img)
                    self.label_image.image = photo_img
                    self.label_name_image.config(text=f"Original: {filename}")

                # Clear existing GLCM images and labels
                for widget in self.glcm_images_frame.winfo_children():
                    widget.destroy()

                # Load GLCM images from the corresponding subfolder
                glcm_subfolder = os.path.join(self.glcm_folder, filename.split('.')[0])
                if os.path.exists(glcm_subfolder):
                    glcm_files = sorted(os.listdir(glcm_subfolder))
                    for i, glcm_file in enumerate(glcm_files):
                        glcm_path = os.path.join(glcm_subfolder, glcm_file)
                        with Image.open(glcm_path) as glcm_img:
                            glcm_img.thumbnail((200, 200))
                            photo_glcm = ImageTk.PhotoImage(glcm_img)
                            glcm_label = tk.Label(self.glcm_images_frame, image=photo_glcm)
                            glcm_label.grid(row=0, column=i, padx=10, pady=10)
                            glcm_label.image = photo_glcm  # Keep reference to avoid garbage collection

                            # Show GLCM image filename below the image
                            glcm_name_label = tk.Label(self.glcm_images_frame, text=glcm_file)
                            glcm_name_label.grid(row=1, column=i, padx=10, pady=5)

            except FileNotFoundError:
                print(f"File not found: {image_path}")

    def show_previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.filenames)
        self.show_current_image()

    def show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.filenames)
        self.show_current_image()

    def run(self):
        self.window.mainloop()

def open_corresponding_image(root_folder):
    app = ImageViewer(root_folder)
    app.run()

# Example usage:
root_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\Example_image'
open_corresponding_image(root_folder)
