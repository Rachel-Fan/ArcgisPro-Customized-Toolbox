import cv2
import os
import numpy as np




import os
import cv2
import numpy as np

def rgba_to_binary_mask(mask_image):
    """
    Convert an RGBA mask image to a single-channel binary mask.
    
    Parameters:
    - mask_image: The RGBA mask image with shape (h, w, 4).
    
    Returns:
    - binary_mask: A single-channel binary mask with 1 for mask areas and 0 for background.
    """
    # Extract the alpha channel (4th channel)
    alpha_channel = mask_image[..., 3]
    
    # Create a binary mask: set pixels with alpha > 0 to 1, background (alpha = 0) to 0
    binary_mask = np.where(alpha_channel > 0, 1, 0).astype(np.uint8)
    
    return binary_mask

def process_masks_in_folder(input_folder, output_folder):
    """
    Loop through all RGBA mask images in a folder, convert each to a binary mask, and save.
    
    Parameters:
    - input_folder: Path to the folder containing RGBA mask images.
    - output_folder: Path to the folder where binary masks will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        # Check if the file is an image (add extensions as needed)
        if filename.endswith('.png'):
            # Load the RGBA image
            image_path = os.path.join(input_folder, filename)
            rgba_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

            # Ensure the image has 4 channels (RGBA)
            if rgba_image is not None and rgba_image.shape[2] == 4:
                # Convert RGBA to binary mask
                binary_mask = rgba_to_binary_mask(rgba_image)

                # Save the binary mask to the output folder
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, binary_mask * 255)  # Scale mask to 0-255 for visibility

                print(f"Processed and saved binary mask for {filename}")
            else:
                print(f"Skipping non-RGBA image: {filename}")

# Example usage

# Define paths to the input mask folder and output folder
input_folder = r'D:\Seagrass\training_result\glcm_output\sam-hq\Alask_mask_only'
output_folder = r'D:\Seagrass\training_result\glcm_output\sam-hq\One_channel_Alask_mask_only'


process_masks_in_folder(input_folder, output_folder)



print("Processing completed.")
