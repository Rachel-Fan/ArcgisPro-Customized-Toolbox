import os
import shutil
import cv2
import numpy as np
import time
from pathlib import Path


def is_valid_image(image_path, threshold):
    """
    Check if the non-black and non-white pixels exceed the threshold percentage.

    :param image_path: Path to the image file.
    :param threshold: Threshold percentage for non-black and non-white pixels (default: 10%).
    :return: True if non-black and non-white pixels are over the threshold, False otherwise.
    """
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"Warning: Could not read {image_path}")
        return False

    total_pixels = image.shape[0] * image.shape[1]

    # Black pixel condition: (0, 0, 0)
    black_pixels = np.all(image == [0, 0, 0], axis=-1).sum()

    # White pixel condition: (255, 255, 255)
    white_pixels = np.all(image == [255, 255, 255], axis=-1).sum()

    # Calculate the ratio of non-black and non-white pixels
    non_black_white_ratio = 1 - ((black_pixels + white_pixels) / total_pixels)

    return non_black_white_ratio > threshold  # Copy if non-black and non-white pixels > threshold


def process_images():
    """
    Process the images based on the hardcoded states and years.
    """
    start_time = time.time()
    total_input_pngs = 0
    total_copied_pngs = 0

    print("\nStarting PNG filtering and copying process...\n")

    for state in STATES:
        for year in YEARS:
            source_dir = Path(INPUT_PATH) / state / year
            if not source_dir.exists():
                print(f"Skipping: {source_dir} (Not Found)")
                continue

            for folder in source_dir.iterdir():
                if folder.is_dir() and folder.name.startswith("image_"):
                    index_folder = folder.parent / folder.name.replace("image_", "index_")

                    if not index_folder.exists():
                        print(f"Skipping {folder}, no matching index folder found.")
                        continue

                    output_state_dir = Path(OUTPUT_FOLDER) / state / "image"
                    output_state_dir.mkdir(parents=True, exist_ok=True)  # Ensure output folder exists

                    png_files = list(folder.glob("*.png"))
                    num_pngs = len(png_files)
                    total_input_pngs += num_pngs

                    copied_pngs = 0
                    for i, image_file in enumerate(png_files, start=1):
                        if is_valid_image(str(image_file), threshold):  # Check if non-black and non-white pixels > threshold
                            shutil.copy(image_file, output_state_dir / image_file.name)
                            copied_pngs += 1

                        if i % 100 == 0:
                            print(f"  Processed {i}/{num_pngs} images in {folder}...")

                    total_copied_pngs += copied_pngs

                    # Print subfolder summary
                    print(f"\nSubfolder: {folder}")
                    print(f"  Total PNGs: {num_pngs}")
                    print(f"  Moved PNGs: {copied_pngs}")

    # Print overall summary
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\n======= Summary =======")
    print(f"Total PNG files found: {total_input_pngs}")
    print(f"Total PNG files moved: {total_copied_pngs}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    print("\nProcessing completed.")


if __name__ == "__main__":
    # Hardcoded paths
    INPUT_PATH = r"D:\Eelgrass_processed_images_2025\ModelData\Data"
    OUTPUT_FOLDER = r"D:\Eelgrass_processed_images_2025\ModelData\image"
    STATES = ["Alaska"]  # Define states
    YEARS = ["2020", "2021", "2022"]  # Define years
    threshold = 0.1  # over 10% non-black and non-white pixels

    process_images()
    print("Processing completed.")