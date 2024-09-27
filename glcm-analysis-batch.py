import os
import time  # Import the time module for timing
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, color
from skimage.feature import graycomatrix, graycoprops

# Define the input folder containing the PNG images and output folder
input_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Oregon\image'
output_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Oregon\glcm'

# Define the distance and angle for the GLCM computation
distances = [3]  # Distance between pixel pairs
angles = [1]     # Angle in radians (0 radians corresponds to horizontal direction)
properties = ['energy']  # List of texture properties to compute

def compute_texture_image(image, distances, angles, properties):
    height, width = image.shape
    texture_images = {prop: np.zeros((height, width)) for prop in properties}

    # Define the window size
    window_size = max(distances) * 2 + 1  # Ensuring the window covers the distance

    # Create a padded image
    padded_image = np.pad(image, pad_width=max(distances), mode='constant', constant_values=0)

    for i in range(height):
        for j in range(width):
            # Extract the window around the current pixel
            window = padded_image[i:i + window_size, j:j + window_size]

            # Compute the GLCM for the window
            glcm = graycomatrix(window, distances, angles, symmetric=True, normed=True)

            # Compute the texture properties from the GLCM
            for prop in properties:
                texture_images[prop][i, j] = graycoprops(glcm, prop).mean()

    return texture_images

def convert_seconds_to_hms(seconds):
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return int(hours), int(minutes), int(seconds)

def process_images(input_folder, output_folder, distances, angles, properties):
    # Get list of all PNG files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    total_images = len(image_files)
    
    # Initialize counter for processed images and start the total time timer
    processed_images = 0
    start_time = time.time()
    
    print(f"Found {total_images} images in the folder.")
    
    # Loop through all PNG files in the input folder
    for filename in image_files:
        image_path = os.path.join(input_folder, filename)

        # Start the timer for processing the individual image
        image_start_time = time.time()

        try:
            # Load and convert the image to grayscale
            image_rgb = io.imread(image_path)
            image_gray = color.rgb2gray(image_rgb)

            # Convert grayscale image to uint8
            image_gray_uint8 = (image_gray * 255).astype(np.uint8)

            # Compute texture images
            texture_images = compute_texture_image(image_gray_uint8, distances, angles, properties)

            # Save the texture images
            for prop in properties:
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
                plt.imsave(output_path, texture_images[prop], cmap='gray')

            # Increment the processed image counter
            processed_images += 1

            # Calculate the time taken for this image
            image_end_time = time.time()
            image_processing_time = image_end_time - image_start_time
            total_elapsed_time = image_end_time - start_time

            # Convert time to hours, minutes, and seconds
            img_hours, img_minutes, img_seconds = convert_seconds_to_hms(image_processing_time)
            total_hours, total_minutes, total_seconds = convert_seconds_to_hms(total_elapsed_time)

            print(f"Processed {filename} in {img_hours}h {img_minutes}m {img_seconds}s. Total time elapsed: {total_hours}h {total_minutes}m {total_seconds}s.")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Summary
    total_time = time.time() - start_time
    total_hours, total_minutes, total_seconds = convert_seconds_to_hms(total_time)
    
    print(f"\nProcessing complete. {processed_images} out of {total_images} images processed and saved.")
    print(f"Total processing time: {total_hours}h {total_minutes}m {total_seconds}s.")

# Call the process_images function
process_images(input_folder, output_folder, distances, angles, properties)
