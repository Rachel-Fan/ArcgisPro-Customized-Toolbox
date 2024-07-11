import os
from PIL import Image

def assign_lighter_color(input_png_path, output_png_path):
    # Open the input PNG image
    image = Image.open(input_png_path)

    # Get the width and height of the image
    width, height = image.size

    # Iterate through each pixel and assign a lighter color
    for y in range(height):
        for x in range(width):
            # Get the pixel value at (x, y)
            pixel = image.getpixel((x, y))

            # Check if the pixel value is 0 (black)
            if pixel == 0:
                # Assign a lighter color (e.g., RGB value of (200, 200, 200))
                image.putpixel((x, y), (200, 200, 200))

    # Save the modified image
    image.save(output_png_path)

    print("Lighter color assignment completed for:", input_png_path)

def process_folder(input_folder, output_folder):
    # Ensure the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all PNG files in the input folder
    png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

    # Process each PNG file
    for png_file in png_files:
        input_png_path = os.path.join(input_folder, png_file)
        output_png_path = os.path.join(output_folder, png_file)
        assign_lighter_color(input_png_path, output_png_path)

def collect_nonzero_pixels(input_png_path):
    # Set the maximum number of pixels before triggering a DecompressionBombWarning
    Image.MAX_IMAGE_PIXELS = None
    
    # Open the input PNG image
    image = Image.open(input_png_path)

    # Get the width and height of the image
    width, height = image.size

    # List to store the coordinates and RGB values of non-zero pixels
    nonzero_pixels = []

    # Iterate through each pixel
    for y in range(height):
        for x in range(width):
            # Get the pixel value at (x, y)
            pixel = image.getpixel((x, y))
            # Check if the pixel value is not (0, 0, 0)
            if pixel != (0, 0, 0):
                # Collect the coordinates and RGB values of non-zero pixels
                nonzero_pixels.append(((x, y), pixel))
                print('non-0 value is found')

    return nonzero_pixels

if __name__ == "__main__":
    print('start')
    # Input PNG path
    input_png_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC_rc_TOOL.png"

    # Collect non-zero pixels
    nonzero_pixels = collect_nonzero_pixels(input_png_path)
    print('run function done')
    # Print collected non-zero pixels
    for pixel_data in nonzero_pixels:
        print(f"Pixel at {pixel_data[0]} has RGB value {pixel_data[1]}")