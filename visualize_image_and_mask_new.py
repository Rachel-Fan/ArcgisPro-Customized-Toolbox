import os
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np

class ImageViewer:
    def __init__(self, root_folder, filenames):
        self.root_folder = root_folder
        self.filenames = filenames
        self.current_index = 0
        self.enhancement = 'original'
        
        self.image_folder = os.path.join(root_folder, "image")
        self.mask_folder = os.path.join(root_folder, "enhanced_mask")
        
        self.window = tk.Tk()
        self.window.title("Image Viewer")
        
        self.left_frame = ttk.Frame(self.window)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.left_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(self.left_frame, yscrollcommand=self.scrollbar.set, height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        for filename in filenames:
            self.listbox.insert(tk.END, filename)
        
        self.scrollbar.config(command=self.listbox.yview)
        
        self.frame_images = ttk.Frame(self.window)
        self.frame_images.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.label_image = tk.Label(self.frame_images)
        self.label_image.grid(row=0, column=0, padx=10)
        
        self.label_name_image = tk.Label(self.frame_images)
        self.label_name_image.grid(row=1, column=0)
        
        self.label_image_hist_eq = tk.Label(self.frame_images)
        self.label_image_hist_eq.grid(row=0, column=1, padx=10)
        
        self.label_name_image_hist_eq = tk.Label(self.frame_images)
        self.label_name_image_hist_eq.grid(row=1, column=1)
        
        self.label_image_2 = tk.Label(self.frame_images)
        self.label_image_2.grid(row=0, column=2, padx=10)
        
        self.label_name_image_2 = tk.Label(self.frame_images)
        self.label_name_image_2.grid(row=1, column=2)
        
        self.label_status = tk.Label(self.window, text="")
        self.label_status.pack(pady=5)

        # Buttons for selecting enhancement type
        self.button_frame = ttk.Frame(self.window)
        self.button_frame.pack(pady=10)
        
        self.btn_original = ttk.Button(self.button_frame, text="Original", command=self.set_original)
        self.btn_original.grid(row=0, column=0, padx=5)
        
        self.btn_clahe = ttk.Button(self.button_frame, text="CLAHE", command=self.set_clahe)
        self.btn_clahe.grid(row=0, column=1, padx=5)
        
        self.btn_gamma = ttk.Button(self.button_frame, text="Gamma Correction", command=self.set_gamma)
        self.btn_gamma.grid(row=0, column=2, padx=5)
        
        self.show_current_image()
        
    def on_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            self.current_index = index
            self.show_current_image()
        
    def show_current_image(self):
        if self.filenames:
            filename = self.filenames[self.current_index]
            image_path = os.path.join(self.image_folder, filename)
            mask_path = os.path.join(self.mask_folder, filename)
            
            try:
                with Image.open(image_path) as img:
                    # Display original image
                    img.thumbnail((600, 600))
                    photo_img = ImageTk.PhotoImage(img)
                    self.label_image.config(image=photo_img)
                    self.label_image.image = photo_img
                    
                    # Apply selected enhancement
                    if self.enhancement == 'clahe':
                        img_enhanced = self.apply_clahe(img)
                    elif self.enhancement == 'gamma':
                        img_enhanced = self.adjust_gamma(img, gamma=1.5)
                    else:
                        img_enhanced = img
                    
                    img_enhanced.thumbnail((600, 600))
                    photo_img_enhanced = ImageTk.PhotoImage(img_enhanced)
                    self.label_image_hist_eq.config(image=photo_img_enhanced)
                    self.label_image_hist_eq.image = photo_img_enhanced
                    
                    # Display mask image
                    with Image.open(mask_path) as mask:
                        mask.thumbnail((600, 600))
                        photo_img_2 = ImageTk.PhotoImage(mask)
                        self.label_image_2.config(image=photo_img_2)
                        self.label_image_2.image = photo_img_2
                    
                    self.label_name_image.config(text=f"Original: {filename}")
                    enhancement_text = f"{self.enhancement.capitalize()}: {filename}"
                    self.label_name_image_hist_eq.config(text=enhancement_text)
                    self.label_name_image_2.config(text=f"Mask: {filename}")
                    
            except FileNotFoundError:
                print(f"File not found. Ensure both {image_path} and {mask_path} exist.")
    
    def set_original(self):
        self.enhancement = 'original'
        self.show_current_image()
        
    def set_clahe(self):
        self.enhancement = 'clahe'
        self.show_current_image()
        
    def set_gamma(self):
        self.enhancement = 'gamma'
        self.show_current_image()
    
    def apply_clahe(self, image):
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(img_array)
        return Image.fromarray(clahe_img)

    def adjust_gamma(self, image, gamma=1.0):
        inv_gamma = 1.0 / gamma
        table = [((i / 255.0) ** inv_gamma) * 255 for i in range(256)]
        table = np.array(table, np.uint8)
        return Image.fromarray(cv2.LUT(np.array(image), table))
    
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
