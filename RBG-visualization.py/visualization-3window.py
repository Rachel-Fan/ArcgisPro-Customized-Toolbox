import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class MultiFolderImageViewer:
    def __init__(self, master, folder1, folder2, folder3, folder4):
        self.master = master
        self.master.title("Multi-Folder Image Viewer")

        self.folders = [folder1, folder2, folder3, folder4]
        self.image_labels = []
        self.caption_labels = []
        self.image_paths = sorted(os.listdir(folder1))  # assumes same filenames across all folders
        self.index = 0

        # Dropdown menu
        self.dropdown_var = tk.StringVar()
        self.dropdown = ttk.Combobox(
            self.master,
            textvariable=self.dropdown_var,
            values=self.image_paths,
            state='readonly'
        )
        self.dropdown.pack(pady=5)
        self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_change)

        # Frame to hold image labels
        self.image_frame = ttk.Frame(self.master)
        self.image_frame.pack()

        # Display placeholders for the four images with captions
        folder_names = ["image", "index", "samhq-ggb", "pasam-ggb"]
        for i in range(4):
            frame = ttk.Frame(self.image_frame)
            frame.grid(row=0, column=i, padx=10, pady=10)

            # image label
            img_label = ttk.Label(frame)
            img_label.pack()
            self.image_labels.append(img_label)

            # caption label
            caption = ttk.Label(frame, text=folder_names[i], font=('Segoe UI', 10, 'bold'))
            caption.pack(pady=5)
            self.caption_labels.append(caption)

        # File name display
        self.filename_label = ttk.Label(self.master, text="")
        self.filename_label.pack(pady=5)

        # Control buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)

        self.prev_button = ttk.Button(button_frame, text="Previous", command=self.show_previous_image)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = ttk.Button(button_frame, text="Next", command=self.show_next_image)
        self.next_button.grid(row=0, column=1, padx=5)

        # Show the first set of images
        self.show_images()

    def show_images(self):
        if not (0 <= self.index < len(self.image_paths)):
            return

        filename = self.image_paths[self.index]
        self.filename_label.config(text=f"Filename: {filename}")
        self.dropdown_var.set(filename)

        for i, folder in enumerate(self.folders):
            image_path = os.path.join(folder, filename)
            if os.path.exists(image_path):
                image = Image.open(image_path).resize((300, 300))
                photo = ImageTk.PhotoImage(image)
                self.image_labels[i].image = photo  # keep reference
                self.image_labels[i].configure(image=photo, text="")
            else:
                self.image_labels[i].configure(image='', text='[Missing]', foreground='red')

        # Button state management
        self.prev_button.config(state=tk.NORMAL if self.index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.index < len(self.image_paths) - 1 else tk.DISABLED)

    def show_next_image(self):
        if self.index < len(self.image_paths) - 1:
            self.index += 1
            self.show_images()

    def show_previous_image(self):
        if self.index > 0:
            self.index -= 1
            self.show_images()

    def on_dropdown_change(self, event):
        selected_filename = self.dropdown_var.get()
        if selected_filename in self.image_paths:
            self.index = self.image_paths.index(selected_filename)
            self.show_images()


if __name__ == "__main__":
    folder1 = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\valid\image"
    folder2 = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\valid\index"
    folder3 = r"\\wsl.localhost\Ubuntu\home\geofly\sam-hq\train\pa-sam-ggb\Alaska-2025\visualize-0522"
    folder4 = r"D:\Eelgrass_processed_images_2025\Trained\image"

    root = tk.Tk()
    app = MultiFolderImageViewer(root, folder1, folder2, folder3, folder4)
    root.mainloop()
