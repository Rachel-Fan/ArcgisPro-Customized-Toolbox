from PIL import Image
import os

def resize_images(input_folder, output_folder, target_size):
    # Check for required folders and subfolders
    drone_image_path = os.path.join(input_folder, 'drone_image', 'png')
    index_tile_path = os.path.join(input_folder, 'index_tile', 'png')
    
    if not os.path.exists(drone_image_path) or not os.path.exists(index_tile_path):
        print("Warning: Required folders or subfolders do not exist.")
        return

    # Directories for output
    output_drone_image = os.path.join(output_folder, 'drone_image')
    output_index_tile = os.path.join(output_folder, 'index_tile')

    # Process PNGs for 'drone_image/png', including band removal
    process_pngs(drone_image_path, output_drone_image, target_size, remove_alpha=True)

    # Process PNGs for 'index_tile/png'
    process_pngs(index_tile_path, output_index_tile, target_size, remove_alpha=False)

def process_pngs(input_folder, output_folder, target_size, remove_alpha=False):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get a list of all PNG files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    
    for image_file in image_files:
        # Open each image
        with Image.open(os.path.join(input_folder, image_file)) as img:
            # Check if removal of the alpha channel is requested
            if remove_alpha and img.mode == 'RGBA':
                img = img.convert('RGB')  # Convert RGBA to RGB to remove the alpha channel
            
            
            # Resize the image using LANCZOS resampling filter
            resized_img = img.resize(target_size, Image.LANCZOS)
            
            # Save the resized image to the output folder
            output_path = os.path.join(output_folder, image_file)
            resized_img.save(output_path)
            print(f"Resized {image_file} successfully.")

# Example usage:
input_folder = r'C:\Users\Rachel\Documents\Seagrass\Dataset\Temp\NC20_cs10'  # Base input folder path
output_folder = r'C:\Users\Rachel\Documents\Seagrass\Dataset\Temp\NC20_cs10\Resized'  # Base output folder path
target_size = (512, 512)  # Desired size for the resized images

resize_images(input_folder, output_folder, target_size)
