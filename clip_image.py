import cv2
import os

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
            output_path = os.path.join(output_folder, f"tile_{y*num_tiles_x + x + 1}.png")
            cv2.imwrite(output_path, tile)

    print("Clipping completed successfully.")

if __name__ == "__main__":
    # Input image path
    input_image_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington\North_Cove\2021\NC_rc_TOOL.tif"
    index_image_path = r""
    
    # Output folder
    output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\NC_2021\Tool_Temp\clip\index"
    
    image_folder = os.path.join(output_folder, f"temp_{prefix}")
    if not os.path.exists(image_folder):
        os.makedirs(image_folder) 
    
    # Clip the image
    clip_image(input_image_path, output_folder)
    
