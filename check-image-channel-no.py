from PIL import Image
import os

import os
import cv2

def check_image_channels(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp')):
            image = cv2.imread(file_path)
            if image is not None:
                channels = image.shape[2] if len(image.shape) == 3 else 1
                print(f"{filename}: {channels} channels")
            else:
                print(f"{filename}: Unable to read image")
        else:
            print(f"{filename}: Not an image file")

# Specify the folder path
folder_path = r'D:\Eelgrass_processed_images_2025\ModelData\Data\Alaska\2019\index_FI_AK_19'
    
check_image_channels(folder_path)


# if __name__ == "__main__":
#     # Specify the folder containing the images
#     image_folder = r'\\wsl.localhost\Ubuntu\home\geofly\sam-hq\train\hqoutput_GGB_vis\Alaska_mask_only_new'
    
#     # Count and list RGBA images
#     count_rgb_rgba_images(image_folder)
