import tifffile
import numpy as np

def remove_5th_channel(image_path, output_path):
    # Load the TIFF image using tifffile
    image = tifffile.imread(image_path)

    if image is None:
        print("Failed to load image. Check the file path.")
        return

    # Check if the image has at least 5 channels
    num_channels = image.shape[2] if len(image.shape) == 3 else 1
    if num_channels < 5:
        print("The image doesn't have 5 channels.")
        return

    # Remove the 5th channel
    new_image = np.delete(image, 4, axis=2)

    # Save the new image as a 4-channel TIFF
    tifffile.imwrite(output_path, new_image)
    print(f"New 4-channel image saved at: {output_path}")

# Example usage
image_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Canada\Underhill\2020\UN_CA_20_Clipped.tif" 

output_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\DroneImageByYear\Canada\2020\UN_CA_20_4channel.tif" 
remove_5th_channel(image_path, output_path)
