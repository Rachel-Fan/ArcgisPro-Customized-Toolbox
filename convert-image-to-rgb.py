
import os
from PIL import Image

def convert_to_rgb(image_path):
    with Image.open(image_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            img.save(image_path)
            print(f'Converted: {image_path}')
        else:
            print(f'Skipped (already RGB): {image_path}')

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                file_path = os.path.join(root, file)
                convert_to_rgb(file_path)

if __name__ == "__main__":
    folder_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Canada\image"
    process_folder(folder_path)
