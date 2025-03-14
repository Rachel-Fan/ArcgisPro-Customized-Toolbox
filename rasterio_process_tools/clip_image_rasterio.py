import os
import numpy as np
import rasterio
from rasterio.windows import Window
from PIL import Image

def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:3])  # Join the first three parts with an underscore
    return prefix

def clip_image(input_image_path, output_folder, tile_size=512, multiply=False):
    # Read the input image using rasterio
    with rasterio.open(input_image_path) as src:
        width, height = src.width, src.height
        num_bands = src.count
        dtype = src.dtypes[0]

        # Calculate the number of tiles in each direction
        num_tiles_x = (width + tile_size - 1) // tile_size
        num_tiles_y = (height + tile_size - 1) // tile_size

        for y in range(num_tiles_y):
            for x in range(num_tiles_x):
                # Define the window for the tile
                left = x * tile_size
                upper = y * tile_size
                right = min(left + tile_size, width)
                lower = min(upper + tile_size, height)

                window = Window(left, upper, right - left, lower - upper)
                tile = src.read(window=window)
                
                # Multiply by 255 if specified and it's a single-band grayscale image
                if multiply and num_bands == 1:
                    tile = (tile * 255.0).clip(0, 255).astype(np.uint8)
                
                # Convert tile to PNG format
                if num_bands == 1:
                    tile = np.squeeze(tile, axis=0)  # Remove single-band axis
                    img = Image.fromarray(tile.astype(np.uint8), mode="L")
                elif num_bands == 4:
                    tile = np.moveaxis(tile, 0, -1)  # Move channels to last axis
                    img = Image.fromarray(tile.astype(np.uint8), mode="RGBA")
                else:
                    tile = np.moveaxis(tile, 0, -1)  # Move channels to last axis
                    img = Image.fromarray(tile.astype(np.uint8), mode="RGB")
                
                # Create output file path
                output_path = os.path.join(output_folder, f"{extract_prefix(input_image_path)}_row{y+1}_col{x+1}.png")
                img.save(output_path, format='PNG')

    print(f"Clipping completed successfully for {input_image_path}.")

def main(input_folder, index_folder, output_folder):
    # Ensure the output directories exist
    os.makedirs(output_folder, exist_ok=True)

    # Process drone images
    if os.path.exists(input_folder):
        for input_image_file in os.listdir(input_folder):
            if input_image_file.endswith('.tif'):
                input_image_path = os.path.join(input_folder, input_image_file)
                print(f"Processing {input_image_path}")
                image_output_folder = os.path.join(output_folder, f"image_{extract_prefix(input_image_path)}")
                os.makedirs(image_output_folder, exist_ok=True)
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
                os.makedirs(index_output_folder, exist_ok=True)
                clip_image(index_image_path, index_output_folder, multiply=True)
                print(f"{index_image_file} - Index image is extracted.")
                print('**********************************')

if __name__ == "__main__":
    years = ["2019", "2020", "2021", "2022"]
    state = "Alaska"
    
    for year in years:
        print(f"Starting processing for the year {year}")
        
        input_folder = f"D:\\Eelgrass_Classified_from_Metashape\\UTM\\DroneImageByYear\\{state}\\{year}"
        index_folder = f"D:\\Eelgrass_processed_images_2025\\ModelData\\{state}\\{year}\\index_tif"
        output_folder = f"D:\\Eelgrass_processed_images_2025\\ModelData\\Data\\{state}\\{year}"
        
        main(input_folder, index_folder, output_folder)
        
    print('All images have been processed for all years.')
