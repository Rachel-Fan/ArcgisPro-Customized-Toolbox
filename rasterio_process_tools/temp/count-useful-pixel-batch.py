import numpy as np
from PIL import Image
import collections
import os
from pathlib import Path

def analyze_image(image_path):
    """
    Analyze the image to calculate the percentage of non-black pixels.

    :param image_path: Path to the image file.
    :return: Percentage of non-black pixels.
    """
    # Open the image file
    image = Image.open(image_path)
    # Convert the image to a numpy array
    image_array = np.array(image)
    
    # Flatten the image array to a 1D array of pixel values
    flattened_image = image_array.flatten()
    
    # Count the occurrences of each pixel value
    pixel_count = collections.Counter(flattened_image)
    
    # Total number of pixels
    total_pixels = flattened_image.size
    
    # Number of non-black pixels (assuming black is 0)
    
    non_black_pixels = total_pixels - pixel_count[0] - pixel_count[255]
    
    # Calculate the percentage of non-black pixels
    non_black_percentage = (non_black_pixels / total_pixels) * 100
    
    return non_black_percentage

def analyze_images_in_folder(folder_path):
    """
    Loop through all images in the specified folder and print the non-black-pixel ratio for each image.

    :param folder_path: Path to the folder containing images.
    """
    # Ensure the folder path is a Path object
    folder_path = Path(folder_path)
    
    # Loop through all PNG files in the folder
    for image_file in folder_path.glob("*.png"):
        # Analyze the image
        non_black_percentage = analyze_image(image_file)
        
        # Print the image name and non-black-pixel ratio
        print(f"{image_file.name}: {non_black_percentage:.2f}%")

def main():
    # Path to the folder containing images
    folder_path = r'D:\Eelgrass_processed_images_2025\ModelData\Data\Alaska\2019\image_FI_AK_19'
    
    # Analyze all images in the folder
    analyze_images_in_folder(folder_path)

if __name__ == "__main__":
    main()