import os
import shutil
from pathlib import Path

def compare_and_copy_images(folder1, folder2, folder3):
    # Create folder3 if it doesn't exist
    Path(folder3).mkdir(parents=True, exist_ok=True)

    # Get all image names (without extension) from folder2
    folder2_images = {Path(f).stem for f in Path(folder2).glob("*.png")}

    # Iterate over all images in folder1
    for image_path in Path(folder1).glob("*.png"):
        if image_path.stem not in folder2_images:
            # If the image name is not in folder2, copy it to folder3
            shutil.copy(image_path, Path(folder3) / image_path.name)
            print(f"Copied: {image_path.name}")

# Paths to your folders
folder1_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Oregon\image"
folder2_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Oregon\glcm"
folder3_path = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Oregon\glcm-working"

# Run the function
compare_and_copy_images(folder1_path, folder2_path, folder3_path)
