import os
import numpy as np
import rasterio
from rasterio.plot import reshape_as_image
import cv2

def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:3])  # Join the first two parts with an underscore
    return prefix

def convert_to_rgb(input_image_path, output_folder):
    # Use rasterio to read the input image
    with rasterio.open(input_image_path) as src:
        input_image = src.read()  # Read the image as a multi-dimensional array

    # Check the number of channels
    num_channels = input_image.shape[0]

    if num_channels < 3:
        raise ValueError(f"Image at {input_image_path} does not have enough channels to form an RGB image.")
    elif num_channels > 3:
        # Keep only the first 3 channels if there are more
        input_image = input_image[:3, :, :]

    # Reshape the image to match OpenCV format (H, W, C)
    input_image = reshape_as_image(input_image)

    # Reassign channels: Channel 1 to Red, Channel 2 to Green, Channel 3 to Blue
    input_image = input_image[:, :, [2, 1, 0]]  # Swap the channels

    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the output path
    output_image_path = os.path.join(output_folder, f"{extract_prefix(input_image_path)}_rgb.tif")

    # Save the image as an RGB PNG file
    cv2.imwrite(output_image_path, input_image)

    print(f"Converted {input_image_path} to RGB and saved to {output_image_path}.")

def main(input_folder, output_folder):
    
    # Process all TIFF images in the input folder
    if os.path.exists(input_folder):
        for input_image_file in os.listdir(input_folder):
            if input_image_file.endswith('.tif'):
                input_image_path = os.path.join(input_folder, input_image_file)
                print(f"Processing {input_image_path}")
                convert_to_rgb(input_image_path, output_folder)
                print(f"{input_image_file} - Converted to RGB.")
                print('**********************************')

if __name__ == "__main__":
    input_folder = "C:\\Users\\GeoFly\\Documents\\rfan\\Seagrass\\Data\\SourceData\\DroneImageByYear\\Canada\\2022"
    output_folder = "C:\\Users\\GeoFly\\Documents\\rfan\\Seagrass\\Data\\Output\\RGB_Images"
    
    main(input_folder, output_folder)
    
    print('All images have been processed.')
