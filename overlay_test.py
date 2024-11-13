import cv2
import numpy as np

# Load the RGB image
rgb_image = cv2.imread(r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Alaska\Alaska\test\image\FI_AK_19_row16_col10.png")
rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)  # Convert to RGB

# Load the RGBA mask
rgba_mask = cv2.imread(r"D:\Seagrass\training_result\glcm_output\sam-hq\Alask_mask_only\FI_AK_19_row16_col10.png", cv2.IMREAD_UNCHANGED)

# Resize the rgba_mask to match the dimensions of rgb_image
rgba_mask = cv2.resize(rgba_mask, (rgb_image.shape[1], rgb_image.shape[0]))

# Separate RGBA channels
r_mask, g_mask, b_mask, alpha_mask = cv2.split(rgba_mask)

# Normalize the alpha mask to the range 0-1
alpha = alpha_mask / 255.0

# Prepare an empty canvas for the blended image
overlay_image = np.zeros_like(rgb_image, dtype=np.uint8)

# Apply the overlay using the alpha channel
for c in range(3):  # Iterate over R, G, B channels
    overlay_image[:, :, c] = (alpha * rgba_mask[:, :, c] + (1 - alpha) * rgb_image[:, :, c]).astype(np.uint8)

# Display or save the final overlaid image
cv2.imwrite(r"D:\Seagrass\training_result\glcm_output\sam-hq\overlaid_image.png", cv2.cvtColor(overlay_image, cv2.COLOR_RGB2BGR))


import cv2
import numpy as np
import os

# Paths to the folders containing images and masks
image_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Alaska\Alaska\test\image"
mask_folder = r"D:\Seagrass\training_result\glcm_output\sam-hq\Alaska_pretrained_mask_only"
output_folder = r"D:\Seagrass\training_result\glcm_output\sam-hq\Alaska_glcm_pretrained"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Set mask color in BGR
mask_color_bgr = np.array([255, 144, 30], dtype=np.uint8)

# Loop through all images in the image folder
for image_filename in os.listdir(image_folder):
    # Construct full paths for the image and the corresponding mask
    image_path = os.path.join(image_folder, image_filename)
    mask_path = os.path.join(mask_folder, image_filename)  # Assume 1-1 filename match

    # Load the RGB image
    rgb_image = cv2.imread(image_path)
    if rgb_image is None:
        print(f"Could not read image {image_path}. Skipping.")
        continue

    # Load the RGBA mask
    rgba_mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    if rgba_mask is None or rgba_mask.shape[2] != 4:
        print(f"Could not read RGBA mask {mask_path}. Skipping.")
        continue

    # Resize mask to match image dimensions if necessary
    if rgba_mask.shape[:2] != rgb_image.shape[:2]:
        rgba_mask = cv2.resize(rgba_mask, (rgb_image.shape[1], rgb_image.shape[0]))

    # Separate RGBA channels
    _, _, _, alpha_mask = cv2.split(rgba_mask)

    # Normalize the alpha mask to the range 0-1
    alpha = alpha_mask / 255.0

    # Prepare an empty canvas for the blended image
    overlay_image = np.copy(rgb_image)

    # Apply the overlay using the mask color and the alpha channel
    for c in range(3):  # Iterate over B, G, R channels
        overlay_image[:, :, c] = (alpha * mask_color_bgr[c] + (1 - alpha) * rgb_image[:, :, c]).astype(np.uint8)

    # Save the resulting image
    output_path = os.path.join(output_folder, image_filename)
    cv2.imwrite(output_path, overlay_image)

    print(f"Processed and saved overlay for {image_filename}")
