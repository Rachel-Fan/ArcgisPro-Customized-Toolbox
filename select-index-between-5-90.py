import os
import shutil
from PIL import Image

def count_non_black_pixels(image_path):
    # Load the image
    img = Image.open(image_path)
    
    # Convert the image to RGBA format if it is not already
    img = img.convert('RGBA')
    
    # Access pixel data
    width, height = img.size
    pixels = img.load()  # Create a pixel access object
    
    # Initialize counter for non-black pixels
    non_black_pixels = 0
    
    # Count non-black pixels
    for y in range(height):
        for x in range(width):
            # Get RGBA values of the pixel at position (x, y)
            pixel = pixels[x, y]
            if pixel != (0, 0, 0, 255):
                non_black_pixels += 1
    
    return non_black_pixels, width * height

def select_and_copy_images(root_dir, destination_folder):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Loop through all subfolders in the root directory
    selected_files = set()
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name.startswith("index_"):
                source_folder = os.path.join(root, dir_name)
                print(f"Processing folder: {source_folder}")
                
                # Loop through all files in the source folder
                for filename in os.listdir(source_folder):
                    if filename.endswith(".png"):  # Check if the file is a PNG image
                        image_path = os.path.join(source_folder, filename)
                        
                        non_black_pixels, total_pixels = count_non_black_pixels(image_path)
                        
                        # Calculate the 10%-90% range for non-black pixels
                        min_non_black_pixels = total_pixels * 0.05
                        max_non_black_pixels = total_pixels * 0.9
                        
                        # Check if the number of non-black pixels is within the 10%-90% range
                        if min_non_black_pixels <= non_black_pixels <= max_non_black_pixels:
                            destination_path = os.path.join(destination_folder, filename)
                            shutil.copy(image_path, destination_path)
                            selected_files.add(filename)
                            print(f"Copied {filename} to {destination_path} because it contains {non_black_pixels} non-black pixels, which is within the 10%-90% range.")
                        else:
                            print(f"{filename} contains {non_black_pixels} non-black pixels, which is not within the 10%-90% range, and was not copied.")
    
    return selected_files

def copy_matching_images(root_dir, selected_files, final_destination_folder):
    # Ensure the final destination folder exists
    os.makedirs(final_destination_folder, exist_ok=True)
    
    # Loop through all subfolders in the root directory
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name.startswith("image_"):
                source_folder = os.path.join(root, dir_name)
                print(f"Processing folder: {source_folder}")
                
                # Loop through all files in the source folder
                for filename in os.listdir(source_folder):
                    if filename in selected_files:
                        image_path = os.path.join(source_folder, filename)
                        destination_path = os.path.join(final_destination_folder, filename)
                        shutil.copy(image_path, destination_path)
                        print(f"Copied {filename} from {source_folder} to {destination_path}.")

def main():
    # Set the root directory and destination directory
    root_dir = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Canada\2019"
    index_destination_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Canada\index"
    final_destination_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Canada\image"
    
    # Select and copy images based on non-black pixel criteria
    selected_files = select_and_copy_images(root_dir, index_destination_folder)
    
    # Copy matching images from image_ folders to final destination folder
    copy_matching_images(root_dir, selected_files, final_destination_folder)

# Run the main function
if __name__ == "__main__":
    main()
    print("All selected images and indexes are copied.")


