import os
import cv2
import numpy as np

# Define paths for the two folders and the output folder
mask_folder = r'D:\Seagrass\training_result\glcm_output\sam-hq\One_channel_Alask_mask_only'
original_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Alaska\Alaska\test\image'
output_folder = r'D:\Seagrass\training_result\glcm_output\sam-hq\Alaska_glcm_red5'

# Loop through each image in the original folder
for filename in os.listdir(original_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # Filter for image files
        # Construct full file paths for the original image and the mask
        original_path = os.path.join(original_folder, filename)
        mask_path = os.path.join(mask_folder, filename)

        # Ensure the corresponding mask file exists
        if not os.path.exists(mask_path):
            print(f"Mask for {filename} not found. Skipping.")
            continue

        # Read the original RGB image and the binary mask
        rgb_image = cv2.imread(original_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        # Resize the mask to match the dimensions of the original image if necessary
        if rgb_image.shape[:2] != mask.shape[:2]:
            mask = cv2.resize(mask, (rgb_image.shape[1], rgb_image.shape[0]))

        # Create an overlay of the same size as the original image, filled with light blue
        light_blue = np.array([255, 144, 30], dtype=np.uint8)  # Light blue in BGR
        overlay = np.zeros_like(rgb_image, dtype=np.uint8)
        overlay[:] = light_blue

        # Apply the mask to the overlay (keeping only the light blue where the mask is 1)
        overlay_masked = cv2.bitwise_and(overlay, overlay, mask=mask)

        # Blend the overlay with the original image
        final_image = cv2.addWeighted(rgb_image, 1, overlay_masked, 0.3, 0)

        # Save the overlayed image
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, final_image)

        print(f"Overlay created for {filename} and saved to {output_path}")

print("Processing completed.")
