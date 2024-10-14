import os
import re
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class ImageViewer:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.image_folder = os.path.join(root_folder, "images")
        self.feature_map_folder = os.path.join(root_folder, "feature_map")
        self.filenames = sorted(os.listdir(self.image_folder))
        self.current_index = 0

        self.window = tk.Tk()
        self.window.title("Image and Feature Map Viewer")

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

        # Right frame for feature maps
        self.right_frame = ttk.Frame(self.window)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.feature_map_images_frame = ttk.Frame(self.right_frame)
        self.feature_map_images_frame.pack(padx=10, pady=10)

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

                # Clear existing feature map images and labels
                for widget in self.feature_map_images_frame.winfo_children():
                    widget.destroy()

                # Load feature map images from the corresponding subfolder
                feature_map_subfolder = os.path.join(self.feature_map_folder, filename.split('.')[0])
                if os.path.exists(feature_map_subfolder):
                    # Filter files using regex for specific filenames
                    pattern = re.compile(r'fm_Conv2d\(3, 64, kernel_size=\(7, 7\), stride=\(2, 2\), padding=\(3, 3\), bias=False\)_(\d{1,2})\.png')
                    feature_map_files = [f for f in sorted(os.listdir(feature_map_subfolder)) if pattern.match(f)]

                    # Ensure only the first 64 files are taken
                    feature_map_files = feature_map_files[:64]

                    for i, feature_map_file in enumerate(feature_map_files):
                        feature_map_path = os.path.join(feature_map_subfolder, feature_map_file)
                        with Image.open(feature_map_path) as feature_img:
                            feature_img.thumbnail((100, 100))  # Smaller thumbnails to fit grid
                            photo_feature = ImageTk.PhotoImage(feature_img)

                            # Calculate row and column for 10x6 grid (first 60 images)
                            if i < 60:
                                row = i // 10  # Standard rows (0-5)
                                col = i % 10  # Standard columns (0-9)
                            else:
                                row = 6  # 11th row
                                col = i % 10  # Columns in 11th row (0-3)

                            # Create frame for each feature map and its label
                            frame = ttk.Frame(self.feature_map_images_frame)
                            frame.grid(row=row*2, column=col, padx=5, pady=5)  # Adjust row to leave space for label

                            # Display feature map image
                            feature_label = tk.Label(frame, image=photo_feature)
                            feature_label.grid(row=0, column=0)
                            feature_label.image = photo_feature  # Keep reference to avoid garbage collection

                            # Extract the digits after the last underscore and before '.png'
                            digit_part = feature_map_file.split('_')[-1].replace('.png', '')

                            # Display only the digits in the label
                            filename_label = tk.Label(frame, text=digit_part, wraplength=100)
                            filename_label.grid(row=1, column=0)

                            
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
