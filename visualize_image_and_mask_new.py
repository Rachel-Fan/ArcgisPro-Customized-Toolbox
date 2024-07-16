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
        
        self.label_image_2 = tk.Label(self.frame_images)
        self.label_image_2.grid(row=0, column=1, padx=10)
        
        self.label_name_image_2 = tk.Label(self.frame_images)
        self.label_name_image_2.grid(row=1, column=1)
        
        self.label_status = tk.Label(self.window, text="")
        self.label_status.pack(pady=5)
        
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
                    with Image.open(mask_path) as mask:
                        img.thumbnail((600,600))
                        photo_img = ImageTk.PhotoImage(img)
                        self.label_image.config(image=photo_img)
                        self.label_image.image = photo_img
                        
                        mask.thumbnail((600, 600))
                        photo_img_2 = ImageTk.PhotoImage(mask)
                        self.label_image_2.config(image=photo_img_2)
                        self.label_image_2.image = photo_img_2
                        
                        self.label_name_image.config(text=f"Image: {filename}")
                        self.label_name_image_2.config(text=f"Mask: {filename}")
                        
            except FileNotFoundError:
                print(f"File not found. Ensure both {image_path} and {mask_path} exist.")
    
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
