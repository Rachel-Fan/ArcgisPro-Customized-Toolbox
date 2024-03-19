import os
import shutil

def select_same_filenames(folder1, folder2):
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)
    
    common_files = set(files1) & set(files2)
    
    return common_files

def copy_files(source_folder, files, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for file in files:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        shutil.copyfile(source_path, destination_path)

if __name__ == "__main__":
    folder1_path = input("Enter the path to folder 1: ")
    folder2_path = input("Enter the path to folder 2: ")
    folder3_path = input("Enter the path to folder 3 (destination): ")
    
    if not os.path.isdir(folder1_path) or not os.path.isdir(folder2_path):
        print("Error: One or both of the provided paths are not valid directories.")
    else:
        common_files = select_same_filenames(folder1_path, folder2_path)
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
