import cv2
import os
import numpy as np
import timer

def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:3])  # Join the first two parts with an underscore
    return prefix

def clip_image(input_image_path, output_folder, tile_size=512, multiply=False):
    # Read the input image
    input_image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)

    # Check if the image is grayscale or has 4 channels (RGBA)
    is_grayscale = len(input_image.shape) == 2 or input_image.shape[2] == 1
    is_rgba = input_image.shape[2] == 4 if len(input_image.shape) == 3 else False

    # Get the dimensions of the input image
    height, width = input_image.shape[:2]

    # Calculate the number of tiles in each direction
    num_tiles_x = (width + tile_size - 1) // tile_size
    num_tiles_y = (height + tile_size - 1) // tile_size

    # Calculate the required size to ensure all tiles are 512x512
    required_width = num_tiles_x * tile_size
    required_height = num_tiles_y * tile_size

    # Create a new image with the required dimensions, and fill it with zeros (black)
    if is_grayscale:
        padded_image = np.zeros((required_height, required_width), dtype=np.uint8)
    elif is_rgba:
        padded_image = np.zeros((required_height, required_width, 4), dtype=np.uint8)
    else:
        padded_image = np.zeros((required_height, required_width, 3), dtype=np.uint8)
    
    # Copy the original image into the padded image
    padded_image[:height, :width] = input_image

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

            # Multiply each cell by 255 if specified and the image is grayscale
            if multiply and is_grayscale:
                tile = cv2.multiply(tile, np.array([255.0]))
                tile = np.clip(tile, 0, 255).astype(np.uint8)

            # Save the tile as a PNG file
            output_path = os.path.join(output_folder, f"{extract_prefix(input_image_path)}_row{y+1}_col{x+1}.png")
            cv2.imwrite(output_path, tile)

    print(f"Clipping completed successfully for {input_image_path}.")

def main(input_folder, index_folder, output_folder):
    
    # Ensure the output directories exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process drone images
    if os.path.exists(input_folder):
        for input_image_file in os.listdir(input_folder):
            if input_image_file.endswith('.tif'):
                input_image_path = os.path.join(input_folder, input_image_file)
                print(f"Processing {input_image_path}")
                image_output_folder = os.path.join(output_folder, f"image_{extract_prefix(input_image_path)}")
                if not os.path.exists(image_output_folder):
                    os.makedirs(image_output_folder)
                clip_image(input_image_path, image_output_folder)
                print(f"{input_image_file} - Drone image has been extracted.")
                print('**********************************')

    # Process index images
    if os.path.exists(index_folder):
        for index_image_file in os.listdir(index_folder):
            if index_image_file.endswith('.tif'):
                print(f"Index image is {index_image_file}")
                index_image_path = os.path.join(index_folder, index_image_file)
                index_prefix = extract_prefix(index_image_path)
                index_output_folder = os.path.join(output_folder, f"index_{index_prefix}")
                if not os.path.exists(index_output_folder):
                    os.makedirs(index_output_folder)
                clip_image(index_image_path, index_output_folder, multiply=True)
                print(f"{index_image_file} - Index image is extracted.")
                print('**********************************')



if __name__ == "__main__":
    years = ["2019", "2020", "2021", "2022"]
    state = "Alaska"
    
    for year in years:
        print(f"Starting processing for the year {year}")

        input_folder = f"D:\\Eelgrass_Classified_from_Metashape\\UTM\\DroneImageByYear\\{state}\\{year}"
        index_folder = f"D:\\Eelgrass_processed_images_2025\\ModelData\\{state}\\\{year}\\index_tif"
        output_folder = f"D:\\Eelgrass_processed_images_2025\\ModelData\\Data\\{state}\\{year}"
        
        main(input_folder, index_folder, output_folder)
        
    print('All images have been processed for all years.')
