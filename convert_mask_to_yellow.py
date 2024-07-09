import numpy as np
import matplotlib.pyplot as plt
import os

def process_image(image_path, save_path):
    # Load the image
    img = plt.imread(image_path)

    # Create a new RGB image; initially set all pixels to black
    rgb_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    # Process each pixel
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            pixel = img[x, y]
            # Set non-black pixels to yellow
            if not np.all(pixel == [0, 0, 0]):
                rgb_image[x, y] = [255, 255, 0]  # RGB for yellow

    # Save the modified image
    plt.imsave(save_path, rgb_image)

def process_all_images(input_folder, output_folder):
    # Ensure output path directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # List all files in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):  # Check for PNG files, adjust if different file types needed
            image_path = os.path.join(input_folder, filename)
            save_path = os.path.join(output_folder, filename)  # Saving with the same filename
            process_image(image_path, save_path)
            print(f"Processed and saved {filename}")


input_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All\index'
output_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All\enhanced_mask'
process_all_images(input_folder, output_folder)
