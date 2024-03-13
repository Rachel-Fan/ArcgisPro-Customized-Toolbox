import os
import shutil

def copy_tif_files_with_19(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Walk through the input folder and its subfolders
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.tif') and data_year_prefix in file:
                #print('find', file)
                src_path = os.path.join(root, file)  # Source path of the .tif file
                dst_path = os.path.join(output_folder, file)  # Destination path in the output folder
                shutil.copy2(src_path, dst_path)  # Copy the file to the output folder
                print(file, 'has been copied')

# Example usage:

print("start")
data_year_prefix = "_20"
input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\Washington"
output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\SourceData\DroneImageByYear\Washington\2019"

copy_tif_files_with_19(input_folder, output_folder)
print("All files copied")