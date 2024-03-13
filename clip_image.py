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
    year = "2019"  # Change the year here
    input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\DroneImageByYear\Washington\{}".format(year)
    index_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Washington\{}\index_tif".format(year)
    output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Washington\{}".format(year)
    
    # Iterate through the files in the input folder
    for input_image_file in os.listdir(input_folder):
        if input_image_file.endswith('.tif'):  # Check if the file ends with ".tif"
        
            input_image_path = os.path.join(input_folder, input_image_file)
            input_prefix = extract_prefix(input_image_path)
            prefix = input_prefix
            print('Input prefix is:', input_prefix)
            
            # Create output folder for input images based on the prefix
            image_output_folder = os.path.join(output_folder, f"image_{input_prefix}")
            if not os.path.exists(image_output_folder):
                os.makedirs(image_output_folder)
            
            # Clip the input image
            clip_image(input_image_path, image_output_folder)
            print(input_image_file, 'Drone image is extracted')
    
    # Iterate through the files in the index folder
    for index_image_file in os.listdir(index_folder):
        if index_image_file.endswith('.tif'):  # Check if the file ends with ".tif"
        
            print('index image is', index_image_file)
            index_image_path = os.path.join(index_folder, index_image_file)
            index_prefix = extract_prefix(index_image_path)
            prefix = index_prefix
            print('Index prefix is:', index_prefix)
            
            # Create output folder for index images based on the prefix
            index_output_folder = os.path.join(output_folder, f"index_{index_prefix}")
            if not os.path.exists(index_output_folder):
                os.makedirs(index_output_folder)
            
            # Clip the index image
            clip_image(index_image_path, index_output_folder)
            print(index_image_file, 'Index image is extracted')
    
    print('All image clip is complete!')
    print('**********************************************')