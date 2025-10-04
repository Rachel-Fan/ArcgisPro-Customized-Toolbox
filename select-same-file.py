import os
import shutil

def select_same_filenames(folder1, folder2):
    # List all files in folder1
    files1 = os.listdir(folder1)
    print(files1)
    
    # Initialize a set to store all png files in folder2 and its subfolders
    files2 = set()
    for root, dirs, files in os.walk(folder2):
        for file in files:
            if file.lower().endswith('.png'):
                files2.add(os.path.relpath(os.path.join(root, file), folder2))
    
    print('files2 are', files2)
    
    # Extract file names without extension for comparison
    base_names1 = {os.path.splitext(file)[0] for file in files1}
    base_names2 = {os.path.splitext(os.path.basename(file))[0] for file in files2}
    
    # Find common file names (without extension)
    common_files = base_names1 & base_names2
    
    # Filter out the files in folder2 that have the same base name as the files in folder1
    common_files_with_extension = {file for file in files2 if os.path.splitext(os.path.basename(file))[0] in common_files}
    
    return common_files_with_extension

def copy_files(source_folder, files, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for file in files:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        destination_dir = os.path.dirname(destination_path)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        shutil.copy(source_path, destination_path)

def main(folder1_path, folder2_path, folder3_path):
    
    common_files = select_same_filenames(folder1_path, folder2_path)
    total_files = len(common_files)
    print(f"Found {total_files} common files.")
    if common_files:
        for file in common_files:
            print(f"Copying {file}...")
            copy_files(folder2_path, [file], folder3_path)
        print("Files copied successfully.")
    else:
        print("No common files found.")
    
    
if __name__ == "__main__":
    print('Start')
    # Prompt user to enter folder paths
    folder1_path = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\valid\image" # folder of file names read from
    folder2_path = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\glcm" # folder we copy from
    folder3_path = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\valid\glcm" # folder we copy to
    
    print('Start selecting')
    main(folder1_path, folder2_path, folder3_path)
    
    print("Done")
