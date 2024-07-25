import os
import shutil

def copy_tif_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through subfolders in the input folder
    for root, dirs, files in os.walk(input_folder):
        for folder in dirs:
            if folder.startswith(folder_type):  # Check if the subfolder starts with "image_"
                subfolder_path = os.path.join(root, folder)
                # Loop through files in the subfolder and copy .tif files to the output folder
                for file in os.listdir(subfolder_path):
                    if file.endswith('.png'):
                        src_path = os.path.join(subfolder_path, file)  # Source path of the .tif file
                        dst_path = os.path.join(output_folder, file)  # Destination path in the output folder
                        shutil.copy2(src_path, dst_path)  # Copy the file to the output folder
                        print(file, 'has been copied')



print("start")
folder_type = "index"  # choose 'image' or 'index'
input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Bodega Bay"

folder_types = ["image", "index"]  # List of folder types
input_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Bodega Bay"

for folder_type in folder_types:
    output_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Alaska\{}".format(folder_type)
    # Place your processing code here
    print("Processing folder type:", folder_type)
    copy_tif_files(input_folder, output_folder)
    
print("All files copied")