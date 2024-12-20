import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class ImageViewer:
    def __init__(self, root_folder_template, additional_folder_template1, additional_folder_template2, additional_folder_template3, additional_folder_template4, additional_folder_template5, additional_folder_template6, states):
        self.window = tk.Tk()  # Initialize the root window first
        self.window.title("Multi-Image Viewer")

        self.root_folder_template = root_folder_template
        self.additional_folder_template1 = additional_folder_template1
        self.additional_folder_template2 = additional_folder_template2
        self.additional_folder_template3 = additional_folder_template3
        self.additional_folder_template4 = additional_folder_template4  # Folder for pa-sam-glcm
        self.additional_folder_template5 = additional_folder_template5  # Folder for hq-glcm
        self.additional_folder_template6 = additional_folder_template6  # Folder for UNet-glcm
        self.states = states
        self.state = tk.StringVar(value=self.states[0])  # Default to the first state
        self.current_index = 0

        # Initialize root folder and additional folders
        self.update_folders(self.state.get())
        self.filenames = sorted(os.listdir(self.image_folder))

        # State dropdown menu
        self.state_dropdown = ttk.Combobox(self.window, textvariable=self.state, values=self.states)
        self.state_dropdown.pack(padx=10, pady=10)
        self.state_dropdown.bind("<<ComboboxSelected>>", self.on_state_change)

        # Display image index and total count at the top center
        self.label_image_index = tk.Label(self.window, text="")
        self.label_image_index.pack(padx=10, pady=10)

        # Left frame for original image and mask
        self.left_frame = ttk.Frame(self.window)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label_image = tk.Label(self.left_frame)
        self.label_image.pack(padx=10, pady=10)

        self.label_mask = tk.Label(self.left_frame)
        self.label_mask.pack(padx=10, pady=10)

        self.label_name_image = tk.Label(self.left_frame)
        self.label_name_image.pack()

        # Next and previous buttons
        self.button_frame = ttk.Frame(self.left_frame)
        self.button_frame.pack(padx=10, pady=10)

        self.btn_prev = ttk.Button(self.button_frame, text="Previous", command=self.show_previous_image)
        self.btn_prev.grid(row=0, column=0, padx=5)

        self.btn_next = ttk.Button(self.button_frame, text="Next", command=self.show_next_image)
        self.btn_next.grid(row=0, column=1, padx=5)

        # Right frame for additional images and labels
        self.right_frame = ttk.Frame(self.window)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.additional_images_frame = ttk.Frame(self.right_frame)
        self.additional_images_frame.pack(padx=10, pady=10)

        self.show_current_image()

    def update_folders(self, state):
        """Update the folder paths based on the selected state."""
        root_folder = self.root_folder_template.format(State=state)
        
        # Dynamically locate the 'image' and 'index' folders under the root folder
        self.image_folder = os.path.join(root_folder, 'image')
        self.mask_folder = os.path.join(root_folder, 'index')
        
        if not os.path.isdir(self.image_folder) or not os.path.isdir(self.mask_folder):
            raise FileNotFoundError(f"Either 'image' or 'index' folder is missing in {root_folder}")

        self.additional_folders = [
            self.additional_folder_template1.format(State=state),  # Unet
            self.additional_folder_template2.format(State=state),  # sam-hq
            self.additional_folder_template3.format(State=state),  # pa-sam
            self.additional_folder_template4.format(State=state),  # pa-sam-glcm
            self.additional_folder_template5.format(State=state),  # hq-glcm
            self.additional_folder_template6.format(State=state)   # UNet-glcm
        ]
        self.filenames = sorted(os.listdir(self.image_folder))

    def show_image(self, label, folder, filename, size=(300, 300)):
        """Helper function to show an image in a given label."""
        image_path = os.path.join(folder, filename)
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size)
                photo_img = ImageTk.PhotoImage(img)
                label.config(image=photo_img)
                label.image = photo_img  # Keep reference to avoid garbage collection
        except FileNotFoundError:
            print(f"File not found: {image_path}")

    def show_current_image(self):
        """Show the current image and mask along with additional images."""
        if self.filenames:
            filename = self.filenames[self.current_index]
            
            # Display original image and mask
            self.show_image(self.label_image, self.image_folder, filename)
            self.show_image(self.label_mask, self.mask_folder, filename)
            self.label_name_image.config(text=f"Image: {filename}")

            # Update the image index display
            total_images = len(self.filenames)
            self.label_image_index.config(text=f"Image {self.current_index + 1} / {total_images}")

            # Clear existing additional images
            for widget in self.additional_images_frame.winfo_children():
                widget.destroy()

            # Load images from the 6 additional folders and display them with labels below
            additional_labels = ["Unet", "sam-hq", "pa-sam", "UNet-glcm", "hq-glcm", "pa-sam-glcm"]
            # additional_labels = ["Unet", "sam-hq", "pa-sam", "UNet-glcm-replace-red-channel", "hq-glcm", "UNet-glcm"]
            # First row (Unet, sam-hq, pa-sam)
            for i in range(3):
                additional_label = tk.Label(self.additional_images_frame)
                additional_label.grid(row=0, column=i, padx=10, pady=10)
                self.show_image(additional_label, self.additional_folders[i], filename, size=(300, 300))
                
                # Add label below the image
                label = tk.Label(self.additional_images_frame, text=additional_labels[i])
                label.grid(row=1, column=i, padx=10, pady=5)

            # Second row for UNet-glcm, hq-glcm, pa-sam-glcm
            for i, col in enumerate([0, 1, 2]):  # Place UNet-glcm, hq-glcm, pa-sam-glcm in columns 1, 2, and 3
                additional_label = tk.Label(self.additional_images_frame)
                additional_label.grid(row=2, column=col, padx=10, pady=10)
                self.show_image(additional_label, self.additional_folders[i + 3], filename, size=(300, 300))

                # Add label below each additional image
                label = tk.Label(self.additional_images_frame, text=additional_labels[i + 3])
                label.grid(row=3, column=col, padx=10, pady=5)

    def show_previous_image(self):
        """Show the previous image."""
        self.current_index = (self.current_index - 1) % len(self.filenames)
        self.show_current_image()

    def show_next_image(self):
        """Show the next image."""
        self.current_index = (self.current_index + 1) % len(self.filenames)
        self.show_current_image()

    def on_state_change(self, event):
        """Handle the state change event from the dropdown."""
        selected_state = self.state.get()
        self.update_folders(selected_state)
        self.current_index = 0  # Reset to the first image for the new state
        self.show_current_image()

    def run(self):
        self.window.mainloop()

def open_corresponding_image():
    states = ["Alaska", "BodegaBay", "Oregon", "Washington"]
    root_folder_template = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\{State}\{State}\test'
    additional_folder_template1 = r'D:\Seagrass\training_result\RGBChannel\{State}\Unet'
    additional_folder_template2 = r'D:\Seagrass\training_result\RGBChannel\{State}\sam-hq'
    additional_folder_template3 = r'D:\Seagrass\training_result\RGBChannel\{State}\pa-sam'
    additional_folder_template5 = r'D:\Seagrass\training_result\glcm_output\sam-hq\{State}'  # Folder for hq-glcm
    #additional_folder_template6 = r'D:\Seagrass\training_result\glcm_output\pa-sam\{State}'  # Folder for pa-sam-glcm
    additional_folder_template6 = r'D:\Seagrass\training_result\glcm_output\pa-sam\{State}'  # Folder for pa-sam-glcm-replacing-red-channel 
    additional_folder_template4 = r'D:\Seagrass\training_result\glcm_output\Unet\{State}'  # Folder for UNet-glcm-replacing-red-channel
    
    
    
    

    app = ImageViewer(root_folder_template, additional_folder_template1, additional_folder_template2, additional_folder_template3, additional_folder_template4, additional_folder_template5, additional_folder_template6, states)
    app.run()


open_corresponding_image()