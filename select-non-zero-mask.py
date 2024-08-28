from PIL import Image
import os
import shutil

# Set the root directory and destination directory
root_dir = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\All"
source_folder = os.path.join(root_dir, "index")
destination_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All\index"

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Loop through all files in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith(".png"):  # Check if the file is a PNG image
        image_path = os.path.join(source_folder, filename)
        
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
        
        # Calculate the total number of pixels and the 10%-90% range for non-black pixels
        total_pixels = width * height
        min_non_black_pixels = total_pixels * 0.1
        max_non_black_pixels = total_pixels * 0.9
        
        # Check if the number of non-black pixels is within the 10%-90% range
        if min_non_black_pixels <= non_black_pixels <= max_non_black_pixels:
            destination_path = os.path.join(destination_folder, filename)
            shutil.copy(image_path, destination_path)
            print(f"Copied {filename} to {destination_path} because it contains {non_black_pixels} non-black pixels, which is within the 10%-90% range.")
        else:
            print(f"{filename} contains {non_black_pixels} non-black pixels, which is not within the 10%-90% range, and was not copied.")

# Print completion message
print("Processing complete.")
