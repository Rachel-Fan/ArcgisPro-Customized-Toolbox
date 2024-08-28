import os
import cv2
import rasterio
import numpy as np

def get_image_statistics(image):
    """Compute statistics for each channel of the image."""
    stats = {}
    for i in range(image.shape[2]):
        channel = image[:, :, i]
        stats[f"Channel {i+1}"] = {
            'mean': np.mean(channel),
            'median': np.median(channel),
            'std': np.std(channel)
        }
    return stats

def analyze_tiff_image(image_path):
    """Analyze a TIFF image using rasterio."""
    with rasterio.open(image_path) as src:
        image = src.read()  # Read the image as a multi-dimensional array
        num_channels = image.shape[0]

        # Transpose image to (H, W, C) format for easier analysis
        image = np.transpose(image, (1, 2, 0))
        
        print(f"Image Path: {image_path}")
        print(f"Number of Channels: {num_channels}")
        
        # Calculate and display statistics for each channel
        stats = get_image_statistics(image)
        for channel, stat in stats.items():
            print(f"{channel}: Mean={stat['mean']}, Median={stat['median']}, Std={stat['std']}")
        
def analyze_png_image(image_path):
    """Analyze a PNG image using OpenCV."""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Could not open or find the image: {image_path}")
    
    # If the image is grayscale, convert it to a 3D array with one channel
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]
    
    num_channels = image.shape[2]
    
    print(f"Image Path: {image_path}")
    print(f"Number of Channels: {num_channels}")
    
    # Calculate and display statistics for each channel
    stats = get_image_statistics(image)
    for channel, stat in stats.items():
        print(f"{channel}: Mean={stat['mean']}, Median={stat['median']}, Std={stat['std']}")
        
def analyze_image(image_path):
    """Determine the file type and analyze the image accordingly."""
    if image_path.lower().endswith('.tif') or image_path.lower().endswith('.tiff'):
        analyze_tiff_image(image_path)
    elif image_path.lower().endswith('.png'):
        analyze_png_image(image_path)
    else:
        print(f"Unsupported file format for {image_path}")

if __name__ == "__main__":
    image_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Canada\test"
    
    # Process all images in the folder
    if os.path.exists(image_folder):
        for image_file in os.listdir(image_folder):
            if image_file.endswith('.tif') or image_file.endswith('.png'):
                image_path = os.path.join(image_folder, image_file)
                analyze_image(image_path)
                print('**********************************')
    else:
        print(f"The folder {image_folder} does not exist.")
