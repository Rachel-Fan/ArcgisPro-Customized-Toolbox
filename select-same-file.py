import os
import shutil

def select_same_filenames(folder1, folder2):
    # List all files in folder1 and folder2
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)
    
    # Extract file names without extension for comparison
    base_names1 = {os.path.splitext(file)[0] for file in files1 if file.lower().endswith('.jpg')}
    base_names2 = {os.path.splitext(file)[0] for file in files2 if file.lower().endswith('.png')}
    
    # Find common file names (without extension)
    common_files = base_names1 & base_names2
    
    # Filter out the PNG files in folder2 that have the same base name as the JPG files in folder1
    common_files_with_extension = {file for file in files2 if os.path.splitext(file)[0] in common_files}
    
    return common_files_with_extension

def copy_files(source_folder, files, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for file in files:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        shutil.copyfile(source_path, destination_path)
        
if __name__ == "__main__":
    print('Start')
    folder1_path = input(r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Subset\Oregon_Subset\image")
    folder2_path = input(r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Oregon\index")
    folder3_path = input(r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Subset\Oregon_Subset\index")
    
    if not os.path.isdir(folder1_path) or not os.path.isdir(folder2_path):
        print("Error: One or both of the provided paths are not valid directories.")
    else:
        common_files = select_same_filenames(folder1_path, folder2_path)
        print('common files are', common_files)
        total_files = len(common_files)
        if common_files:
            print("Common files found in both folders:")
            progress = 0
            for i, file in enumerate(common_files, start=1):
                print(file)
                progress = i / total_files * 100
                print(f"Progress: {progress:.2f}%")
                # Copy the file from folder2 to folder3
                copy_files(folder2_path, [file], folder3_path)
            print("Files copied successfully.")
        else:
            print("No common files found in both folders.")
