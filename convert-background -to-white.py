import cv2
import numpy as np
import os

def convert_black_to_white(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)

    # Define the black color range
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([0, 0, 0])

    # Create a mask for black color
    mask = cv2.inRange(image, lower_black, upper_black)

    # Change the black pixels to white
    image[mask > 0] = [255, 255, 255]

    # Save the modified image
    cv2.imwrite(output_path, image)

def process_folder(input_folder, output_folder):
    # Walk through all files and folders in the directory
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.png'):
                input_path = os.path.join(root, file)
                
                # Create corresponding output path
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                
                # Create output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Convert black to white and save
                convert_black_to_white(input_path, output_path)
                print(f"Processed: {input_path} -> {output_path}")

# Example usage
input_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Canada\2022'
output_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Canada\2022-white'

process_folder(input_folder, output_folder)
