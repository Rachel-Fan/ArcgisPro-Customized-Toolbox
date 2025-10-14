import os
import time
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, color
from skimage.feature import graycomatrix
from scipy.stats import entropy
from concurrent.futures import ProcessPoolExecutor

# Define the input folder containing the PNG images and output folder
input_folder = r'D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\image'
output_folder = r'D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\glcm'

# Define the distance and angle for the GLCM computation
distances = [3]  # Distance between pixel pairs
angles = [0]     # Angle in radians (0 radians corresponds to horizontal direction)

def compute_glcm_entropy(image, distances, angles):
    height, width = image.shape
    entropy_image = np.zeros((height, width))  # Output image for entropy values

    # Define the window size
    window_size = max(distances) * 2 + 1  # Ensuring the window covers the distance

    # Create a padded image
    padded_image = np.pad(image, pad_width=max(distances), mode='constant', constant_values=0)

    for i in range(height):
        for j in range(width):
            # Extract the window around the current pixel
            window = padded_image[i:i + window_size, j:j + window_size]

            # Compute the GLCM for the window
            glcm = graycomatrix(window, distances=distances, angles=angles, symmetric=True, normed=True)

            # Compute the entropy for the GLCM
            glcm_entropy = -np.sum(glcm * np.log2(glcm + (glcm == 0)))  # Add epsilon to avoid log2(0)
            entropy_image[i, j] = glcm_entropy

    return entropy_image

def convert_seconds_to_hms(seconds):
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return int(hours), int(minutes), int(seconds)

def process_single_image(filename):
    try:
        image_path = os.path.join(input_folder, filename)

        # Start the timer for processing the individual image
        image_start_time = time.time()

        # Load and convert the image to grayscale
        image_rgb = io.imread(image_path)
        if image_rgb is None:
            print(f"Failed to load image {filename}. Skipping.")
            return filename, None
        
        print(f"Image {filename} loaded successfully.")

        image_gray = color.rgb2gray(image_rgb)

        # Convert grayscale image to uint8
        image_gray_uint8 = (image_gray * 255).astype(np.uint8)

        # Compute the GLCM entropy
        entropy_image = compute_glcm_entropy(image_gray_uint8, distances, angles)

        # Save the entropy image
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
        plt.imsave(output_path, entropy_image, cmap='gray')

        print(f"Saved entropy image for {filename}.")

        # Calculate the time taken for this image
        image_end_time = time.time()
        image_processing_time = image_end_time - image_start_time

        return filename, image_processing_time

    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return filename, None

def process_images(input_folder, output_folder, distances, angles, max_workers=6):
    # Get list of all PNG files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    total_images = len(image_files)
    
    # Check if no images are found
    if total_images == 0:
        print(f"No PNG images found in {input_folder}.")
        return
    
    print(f"Found {total_images} images in the folder.")

    # Initialize counter for processed images and start the total time timer
    start_time = time.time()

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Use ProcessPoolExecutor to parallelize the processing of images
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks to the executor
        results = list(executor.map(process_single_image, image_files))

    # Gather results and display processing times
    processed_images = 0
    for filename, processing_time in results:
        if processing_time is not None:
            processed_images += 1
            img_hours, img_minutes, img_seconds = convert_seconds_to_hms(processing_time)
            print(f"Processed {filename} in {img_hours}h {img_minutes}m {img_seconds}s.")

    # Calculate total elapsed time
    total_time = time.time() - start_time
    total_hours, total_minutes, total_seconds = convert_seconds_to_hms(total_time)

    # Summary
    print(f"\nProcessing complete. {processed_images} out of {total_images} images processed and saved.")
    print(f"Total processing time: {total_hours}h {total_minutes}m {total_seconds}s.")

if __name__ == "__main__":
    process_images(input_folder, output_folder, distances, angles, max_workers=4)
