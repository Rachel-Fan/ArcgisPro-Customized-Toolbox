import cv2
import os

def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:2])  # Join the first two parts with an underscore
    
    return prefix

def clip_image(input_image_path, output_folder, tile_size=512):
    # Read the input image
    input_image = cv2.imread(input_image_path)

    # Get the dimensions of the input image
    height, width, _ = input_image.shape

    # Calculate the number of tiles in each direction
    num_tiles_x = width // tile_size
    num_tiles_y = height // tile_size

    # Loop through each tile
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            # Calculate the tile coordinates
            left = x * tile_size
            upper = y * tile_size
            right = left + tile_size
            lower = upper + tile_size

            # Crop the tile from the input image
            tile = input_image[upper:lower, left:right]

            # Save the tile as a PNG file
            output_path = os.path.join(output_folder, f"{prefix}_tile_{y*num_tiles_x + x + 1}.png")
            cv2.imwrite(output_path, tile)

    print("Clipping completed successfully.")

if __name__ == "__main__":
    # Input image path
    input_image_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\Beach_Haven\2019\BH_19_Clipped.tif"
    index_image_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Washington\2019\BH_19_index_tif.tif"
    
    prefix = extract_prefix(input_image_path)
    print('prefix is', prefix)
    
    # Output folder
    output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Washington\2019"
    
    image_folder = os.path.join(output_folder, f"image_{prefix}")
    if not os.path.exists(image_folder):
        os.makedirs(image_folder) 
    
    index_folder = os.path.join(output_folder, f"index_{prefix}")
    if not os.path.exists(index_folder):
        os.makedirs(index_folder) 
    
    
    # Clip the image
    clip_image(input_image_path, image_folder)
    print('drone images are extracted')
    clip_image(index_image_path, index_folder)
    print('index image is extracted')
    
