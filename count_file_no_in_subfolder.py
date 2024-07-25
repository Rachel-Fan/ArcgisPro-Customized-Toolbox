import os
import glob

def count_png_files(folder):
    # Prepare to count PNG files in each subfolder
    for root, dirs, files in os.walk(folder):
        # Filter only PNG files
        png_files = [file for file in files if file.lower().endswith('.png')]
        # Get count of PNG files
        png_count = len(png_files)
        # Print the subfolder path and count of PNG files
        print(f"{root}: {png_count} PNG files")

if __name__ == "__main__":
    input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Bodega Bay\New_0717"  # Replace with your actual folder path
    count_png_files(input_folder)
