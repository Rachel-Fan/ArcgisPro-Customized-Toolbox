import os
import shutil

def get_reference_base_names(folder1):
    """Return a set of base filenames (without extension) from folder1."""
    files = os.listdir(folder1)
    base_names = {os.path.splitext(file)[0] for file in files}
    print(f"Reference base names (from folder1): {base_names}")
    return base_names

def find_matching_files_flat(folder2, reference_base_names):
    """Find full paths of matching files under all 'index_*' subfolders of folder2."""
    matched_files = []
    for root, dirs, _ in os.walk(folder2):
        for dirname in dirs:
            if dirname.startswith("index_"):
                index_folder_path = os.path.join(root, dirname)
                for sub_root, _, files in os.walk(index_folder_path):
                    for file in files:
                        if file.lower().endswith('.png'):
                            base_name = os.path.splitext(file)[0]
                            if base_name in reference_base_names:
                                full_path = os.path.join(sub_root, file)
                                matched_files.append(full_path)
    return matched_files

def copy_files_flat(source_file_paths, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    for source_path in source_file_paths:
        filename = os.path.basename(source_path)
        destination_path = os.path.join(destination_folder, filename)
        shutil.copy(source_path, destination_path)
        print(f"Copied {filename} to {destination_folder}")

def main(folder1_path, folder2_path, folder3_path):
    reference_base_names = get_reference_base_names(folder1_path)
    matched_files = find_matching_files_flat(folder2_path, reference_base_names)

    print(f"Found {len(matched_files)} matching files in 'index_' folders.")
    
    if matched_files:
        copy_files_flat(matched_files, folder3_path)
        print("Files copied successfully.")
    else:
        print("No matching files found.")


if __name__ == "__main__":
    print('Start')
    folder1_path = r"D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\image" # folder of file names read from
    folder2_path = r"D:\Eelgrass_processed_images_2025\ModelData\Data_clipped_by_sites\Washington" # folder we copy from
    folder3_path = r"D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Wanshington\index" # folder we copy to
    
    print('Start selecting')
    main(folder1_path, folder2_path, folder3_path)
    
    print("Done")
