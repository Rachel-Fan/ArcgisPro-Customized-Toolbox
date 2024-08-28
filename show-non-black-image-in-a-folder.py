import os
from PIL import Image

# Define the directory containing the images
directory = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Bodega Bay\2022\index_BL_BB_22"

# Initialize a list to store image names that are not all black
not_all_black_images = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        image_path = os.path.join(directory, filename)
        
        # Load the image
        img = Image.open(image_path)

        # Convert the image to RGBA format if it is not already
        img = img.convert('RGBA')

        # Access pixel data
        width, height = img.size
        pixels = img.load()  # Create a pixel access object

        # Initialize counters
        black_pixels = 0
        non_black_pixels = 0

        # Count black and non-black pixels
        for y in range(height):
            for x in range(width):
                # Get RGBA values of the pixel at position (x, y)
                pixel = pixels[x, y]
                if pixel == (0, 0, 0, 255):
                    black_pixels += 1
                else:
                    non_black_pixels += 1

        
        # Check if the image is not entirely black
        if non_black_pixels > 0:
            not_all_black_images.append(filename)
            print(f"Number of black pixels: {black_pixels}")
            print(f"Number of non-black pixels: {non_black_pixels}")

# Print the names of images that are not all black
print("Number of non-black images is", len(not_all_black_images))
print("Images that are not all black:")

for image_name in not_all_black_images:
    print(image_name)
