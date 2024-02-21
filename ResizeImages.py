from PIL import Image
import os

def resize_images(input_folder, output_folder, target_size=(1183, 1183)):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get a list of all PNG files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    
    for image_file in image_files:
        # Open each image
        with Image.open(os.path.join(input_folder, image_file)) as img:
            # Resize the image using LANCZOS resampling filter
            resized_img = img.resize(target_size, Image.LANCZOS)
            
            # Save the resized image to the output folder
            output_path = os.path.join(output_folder, image_file)
            resized_img.save(output_path)
            print(f"Resized {image_file} successfully.")

# Example usage:
input_folder = r'C:\Users\Rachel\Documents\Seagrass\Dataset\Temp\NC20_cs20\ReadyDataset\label_images'
output_folder = r'C:\Users\Rachel\Documents\Seagrass\Dataset\Temp\NC20_cs20\ReadyDataset\Resize_mask'
resize_images(input_folder, output_folder)
