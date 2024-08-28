import os
import numpy as np
import cv2
from osgeo import gdal

def extract_prefix(input_image_path):
    return os.path.splitext(os.path.basename(input_image_path))[0]

def clip_image(input_image_path, output_folder, tile_size=512):
    # Read the input image using GDAL to handle TIFF files correctly
    input_image_dataset = gdal.Open(input_image_path)
    input_image = input_image_dataset.ReadAsArray()
    
    # If the image is grayscale, add a channel dimension
    if len(input_image.shape) == 2:
        input_image = np.expand_dims(input_image, axis=2)

    # Get the dimensions of the input image
    height, width = input_image.shape[:2]
    channels = input_image.shape[2] if len(input_image.shape) == 3 else 1

    # Calculate the number of tiles in each direction
    num_tiles_x = (width + tile_size - 1) // tile_size
    num_tiles_y = (height + tile_size - 1) // tile_size

    # Calculate the required size to ensure all tiles are 512x512
    required_width = num_tiles_x * tile_size
    required_height = num_tiles_y * tile_size

    # Create a new image with the required dimensions, and fill it with zeros (black)
    padded_image = np.zeros((required_height, required_width, channels), dtype=input_image.dtype)
    
    # Copy the original image into the padded image
    padded_image[:height, :width, :] = input_image

    # Loop through each tile
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            # Calculate the tile coordinates
            left = x * tile_size
            upper = y * tile_size
            right = left + tile_size
            lower = upper + tile_size

            # Crop the tile from the padded image
            tile = padded_image[upper:lower, left:right]

            # Save the tile as a PNG file
            output_path = os.path.join(output_folder, f"{extract_prefix(input_image_path)}_row{y+1}_col{x+1}.png")
            cv2.imwrite(output_path, tile)

    print(f"Clipping completed successfully for {input_image_path}.")

# Example usage
clip_image(r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Canada\2022\index_PR_CA_22\PR_CA_22_row9_col7.tif", r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Canada\2022\clipped_tiles")
