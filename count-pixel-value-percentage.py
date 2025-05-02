import numpy as np
from PIL import Image
import collections

def analyze_image(image_path):
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
    non_black_pixels = total_pixels - pixel_count[0]
    
    # Calculate the percentage of non-black pixels
    non_black_percentage = (non_black_pixels / total_pixels) * 100
    
    return pixel_count, non_black_percentage

def main():
    # Path to the input PNG image
    image_path = r'D:\Eelgrass_processed_images_2025\ModelData\Data\Alaska\2019\image_FI_AK_19\FI_AK_19_row2_col14.png'
    
    # Analyze the image
    pixel_count, non_black_percentage = analyze_image(image_path)
    
    # Print the results
    print("Pixel Values Count:")
    for pixel_value, count in pixel_count.items():
        print(f"Pixel Value {pixel_value}: {count}")
    
    print(f"\nPercentage of Non-Black Pixels: {non_black_percentage:.2f}%")

if __name__ == "__main__":
    main()
