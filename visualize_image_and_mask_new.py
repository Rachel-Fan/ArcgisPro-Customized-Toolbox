import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class ImageViewer:
    def __init__(self, root_folder, filenames):
        self.root_folder = root_folder
        self.filenames = filenames
        self.current_index = 0
        
        self.image_folder = os.path.join(root_folder, "image")
        self.mask_folder = os.path.join(root_folder, "enhanced_mask")
        
        self.window = tk.Tk()
        self.window.title("Image Viewer")
        
        
        self.frame_images = ttk.Frame(self.window)
        self.frame_images.pack(padx=10, pady=10)
        
        self.label_image = tk.Label(self.frame_images)
        self.label_image.grid(row=0, column=0, padx=10)
        
        self.label_image_2 = tk.Label(self.frame_images)
        self.label_image_2.grid(row=0, column=1, padx=10)
        
        self.label_status = tk.Label(self.window, text="")
        self.label_status.pack(pady=5)
        
        self.frame_buttons = ttk.Frame(self.window)
        self.frame_buttons.pack(pady=10)
        
        self.button_prev = ttk.Button(self.frame_buttons, text="Previous", command=self.show_previous_image)
        self.button_prev.grid(row=0, column=0, padx=5)
        
        self.button_next = ttk.Button(self.frame_buttons, text="Next", command=self.show_next_image)
        self.button_next.grid(row=0, column=1, padx=5)
        
        self.show_current_image()
        
    def show_current_image(self):
        filename = self.filenames[self.current_index]
        image_path = os.path.join(self.image_folder, filename)
        mask_path = os.path.join(self.mask_folder, filename)
        
        try:
            with Image.open(image_path) as img:
                with Image.open(mask_path) as mask:
                    # Resize image to fit within a reasonable display size
                    img.thumbnail((600,600))
                    photo_img = ImageTk.PhotoImage(img)
                    self.label_image.config(image=photo_img)
                    self.label_image.image = photo_img  # Keep a reference to avoid garbage collection
                    
                    mask.thumbnail((600, 600))
                    photo_img_2 = ImageTk.PhotoImage(mask)
                    self.label_image_2.config(image=photo_img_2)
                    self.label_image_2.image = photo_img_2  # Keep a reference to avoid garbage collection
                    
                    self.label_status.config(text=f"Image {self.current_index + 1} / {len(self.filenames)}")
        except FileNotFoundError:
            print(f"File not found. Ensure both {image_path} and {mask_path} exist.")
    
    def show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.filenames)
        self.show_current_image()
        
    def show_previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.filenames)
        self.show_current_image()
    
    def run(self):
        self.window.mainloop()

def open_corresponding_image(root_folder):
    image_folder = os.path.join(root_folder, "image")
    filenames = os.listdir(image_folder)
    app = ImageViewer(root_folder, filenames)
    app.run()

# Example usage:
root_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All'
open_corresponding_image(root_folder)