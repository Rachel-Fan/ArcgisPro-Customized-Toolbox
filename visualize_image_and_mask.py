import matplotlib.pyplot as plt
import os
from PIL import Image

def display_images(image_folder, mask_folder, filename):
    # Construct full paths for the image and the mask
    image_path = os.path.join(image_folder, filename)
    mask_path = os.path.join(mask_folder, filename)
    
    # Load the image and the mask
    try:
        with Image.open(image_path) as img:
            with Image.open(mask_path) as mask:
                # Display the image and the mask side by side
                fig, axes = plt.subplots(1, 2, figsize=(12, 6))
                axes[0].imshow(img)
                axes[0].set_title('Original Image')
                axes[0].axis('off')

                axes[1].imshow(mask)
                axes[1].set_title('Enhanced Mask')
                axes[1].axis('off')

                plt.show()
    except FileNotFoundError:
        print(f"File not found. Ensure both {image_path} and {mask_path} exist.")

def open_corresponding_image(root_folder, filename):
    image_folder = os.path.join(root_folder, "image")
    mask_folder = os.path.join(root_folder, "enhanced_mask")
    display_images(image_folder, mask_folder, filename)

# Example usage:
root_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All'  

filename = 'JF_20_tile_314.png'  # Replace with the filename of the image you want to open
open_corresponding_image(root_folder, filename)
