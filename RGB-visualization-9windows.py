import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class ImageViewer:
    def __init__(self, root_folder_template, additional_folder_template1, additional_folder_template2, additional_folder_template3, additional_folder_template4, additional_folder_template5, additional_folder_template6, additional_folder_template7, additional_folder_template8, additional_folder_template9, states):
        self.window = tk.Tk()
        self.window.title("Multi-Image Viewer")

        self.root_folder_template = root_folder_template
        self.additional_folder_template1 = additional_folder_template1
        self.additional_folder_template2 = additional_folder_template2
        self.additional_folder_template3 = additional_folder_template3
        self.additional_folder_template4 = additional_folder_template4
        self.additional_folder_template5 = additional_folder_template5
        self.additional_folder_template6 = additional_folder_template6
        self.additional_folder_template7 = additional_folder_template7
        self.additional_folder_template8 = additional_folder_template8
        self.additional_folder_template9 = additional_folder_template9
        self.states = states
        self.state = tk.StringVar(value=self.states[0])
        self.current_index = 0

        self.update_folders(self.state.get())
        self.filenames = sorted(os.listdir(self.image_folder))

        self.state_dropdown = ttk.Combobox(self.window, textvariable=self.state, values=self.states)
        self.state_dropdown.pack(padx=10, pady=10)
        self.state_dropdown.bind("<<ComboboxSelected>>", self.on_state_change)

        self.label_image_index = tk.Label(self.window, text="")
        self.label_image_index.pack(padx=10, pady=10)

        self.left_frame = ttk.Frame(self.window)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label_image = tk.Label(self.left_frame)
        self.label_image.pack(padx=10, pady=10)

        self.label_mask = tk.Label(self.left_frame)
        self.label_mask.pack(padx=10, pady=10)

        self.label_name_image = tk.Label(self.left_frame)
        self.label_name_image.pack()

        self.button_frame = ttk.Frame(self.left_frame)
        self.button_frame.pack(padx=10, pady=10)

        self.btn_prev = ttk.Button(self.button_frame, text="Previous", command=self.show_previous_image)
        self.btn_prev.grid(row=0, column=0, padx=5)

        self.btn_next = ttk.Button(self.button_frame, text="Next", command=self.show_next_image)
        self.btn_next.grid(row=0, column=1, padx=5)

        self.right_frame = ttk.Frame(self.window)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.additional_images_frame = ttk.Frame(self.right_frame)
        self.additional_images_frame.pack(padx=10, pady=10)

        self.show_current_image()

    def update_folders(self, state):
        root_folder = self.root_folder_template.format(State=state)
        self.image_folder = os.path.join(root_folder, 'image')
        self.mask_folder = os.path.join(root_folder, 'index')

        if not os.path.isdir(self.image_folder) or not os.path.isdir(self.mask_folder):
            raise FileNotFoundError(f"Either 'image' or 'index' folder is missing in {root_folder}")

        self.additional_folders = [
            self.additional_folder_template1.format(State=state),
            self.additional_folder_template2.format(State=state),
            self.additional_folder_template3.format(State=state),
            self.additional_folder_template4.format(State=state),
            self.additional_folder_template5.format(State=state),
            self.additional_folder_template6.format(State=state),
            self.additional_folder_template7.format(State=state),
            self.additional_folder_template8.format(State=state),
            self.additional_folder_template9.format(State=state)
        ]
        self.filenames = sorted(os.listdir(self.image_folder))

    def show_image(self, label, folder, filename, size=(200, 200)):
        image_path = os.path.join(folder, filename)
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size)
                photo_img = ImageTk.PhotoImage(img)
                label.config(image=photo_img)
                label.image = photo_img
        except FileNotFoundError:
            print(f"File not found: {image_path}")

    def show_current_image(self):
        if self.filenames:
            filename = self.filenames[self.current_index]

            self.show_image(self.label_image, self.image_folder, filename)
            self.show_image(self.label_mask, self.mask_folder, filename)
            self.label_name_image.config(text=f"Image: {filename}")

            total_images = len(self.filenames)
            self.label_image_index.config(text=f"Image {self.current_index + 1} / {total_images}")

            for widget in self.additional_images_frame.winfo_children():
                widget.destroy()

            additional_labels = ["Unet", "sam-hq", "pa-sam", "UNet-glcm", "hq-glcm", "pa-sam-glcm", "Unet_pretrained", "sam_hq-pretrained", "pa-sam-pretrained"]
            
            for i in range(3):
                additional_label = tk.Label(self.additional_images_frame)
                additional_label.grid(row=0, column=i, padx=10, pady=10)
                self.show_image(additional_label, self.additional_folders[i], filename, size=(200, 200))
                label = tk.Label(self.additional_images_frame, text=additional_labels[i])
                label.grid(row=1, column=i, padx=10, pady=5)

            for i in range(3):
                additional_label = tk.Label(self.additional_images_frame)
                additional_label.grid(row=2, column=i, padx=10, pady=10)
                self.show_image(additional_label, self.additional_folders[i + 3], filename, size=(200, 200))
                label = tk.Label(self.additional_images_frame, text=additional_labels[i + 3])
                label.grid(row=3, column=i, padx=10, pady=5)

            for i in range(3):
                additional_label = tk.Label(self.additional_images_frame)
                additional_label.grid(row=4, column=i, padx=10, pady=10)
                self.show_image(additional_label, self.additional_folders[i + 6], filename, size=(200, 200))
                label = tk.Label(self.additional_images_frame, text=additional_labels[i + 6])
                label.grid(row=5, column=i, padx=10, pady=5)

    def show_previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.filenames)
        self.show_current_image()

    def show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.filenames)
        self.show_current_image()

    def on_state_change(self, event):
        selected_state = self.state.get()
        self.update_folders(selected_state)
        self.current_index = 0
        self.show_current_image()

    def run(self):
        self.window.mainloop()

def open_corresponding_image():
    states = ["Alaska", "BodegaBay", "Oregon", "Washington"]
    root_folder_template = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\{State}\{State}\test'
    additional_folder_template1 = r'D:\Seagrass\training_result\RGBChannel\{State}\Unet'
    additional_folder_template2 = r'D:\Seagrass\training_result\RGBChannel\{State}\sam-hq'
    additional_folder_template3 = r'D:\Seagrass\training_result\RGBChannel\{State}\pa-sam'
    additional_folder_template4 = r'D:\Seagrass\training_result\glcm_output\Unet\{State}'
    additional_folder_template5 = r'D:\Seagrass\training_result\glcm_output\sam-hq\{State}'
    additional_folder_template6 = r'D:\Seagrass\training_result\glcm_output\pa-sam\{State}'
    additional_folder_template7 = r'D:\Seagrass\training_result\glcm_output\Unet\{State}_glcm_pretrained'
    additional_folder_template8 = r'D:\Seagrass\training_result\glcm_output\sam-hq\{State}_glcm_pretrained'
    additional_folder_template9 = r'D:\Seagrass\training_result\glcm_output\pa-sam\{State}_glcm_pretrained'

    app = ImageViewer(root_folder_template, additional_folder_template1, additional_folder_template2, additional_folder_template3,
                      additional_folder_template4, additional_folder_template5, additional_folder_template6,
                      additional_folder_template7, additional_folder_template8, additional_folder_template9, states)
    app.run()

open_corresponding_image()
