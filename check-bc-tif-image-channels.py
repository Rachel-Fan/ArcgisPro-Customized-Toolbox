import tifffile
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import generic_filter

def std_deviation_filter(image, size):
    # Apply a standard deviation filter to each channel
    return generic_filter(image, np.std, size=size)

def display_rgb_channels_with_std_filter(image_path, filter_size=3):
    # Load the TIFF image using tifffile
    image = tifffile.imread(image_path)

    if image is None:
        print("Failed to load image. Check the file path.")
        return

    # Get the number of channels
    num_channels = image.shape[2] if len(image.shape) == 3 else 1

    if num_channels < 3:
        print("The image doesn't have enough channels to display as RGB.")
        return

    # Assuming the first three channels are R, G, and B
    rgb_image = image[:, :, :3]

    # Apply standard deviation filter to each channel
    r_filtered = std_deviation_filter(rgb_image[:, :, 0], size=filter_size)
    g_filtered = std_deviation_filter(rgb_image[:, :, 1], size=filter_size)
    b_filtered = std_deviation_filter(rgb_image[:, :, 2], size=filter_size)

    # Stack the filtered channels back into an RGB image
    filtered_rgb_image = np.stack([r_filtered, g_filtered, b_filtered], axis=-1)

    # Display the RGB image with the standard deviation filter applied
    plt.figure(figsize=(8, 8))
    plt.imshow(filtered_rgb_image)
    plt.title("RGB Image with Standard Deviation Filter")
    plt.axis('off')
    plt.show()

# Example usage
image_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Canada\Duck\2020\DU_CA_20_Duck20.tif" 

display_rgb_channels_with_std_filter(image_path, filter_size=3)




