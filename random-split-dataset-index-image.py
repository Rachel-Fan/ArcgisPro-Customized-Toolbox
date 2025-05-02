import os
import shutil
import random

def split_data(source_folder, output_folder, train_size=0.7, valid_size=0.2):
    # Ensure the randomness is reproducible
    random.seed(42)
    
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"The source folder {source_folder} does not exist.")
        return
    
    # Create output folders if they don't exist
    train_folder = os.path.join(output_folder, 'train')
    valid_folder = os.path.join(output_folder, 'valid')
    test_folder = os.path.join(output_folder, 'test')
    
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(valid_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    
    # Get all files in the source folder
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    random.shuffle(files)
    
    # Split files into train, valid, test according to specified sizes
    total_files = len(files)
    train_files = files[:int(total_files * train_size)]
    valid_files = files[int(total_files * train_size):int(total_files * (train_size + valid_size))]
    test_files = files[int(total_files * (train_size + valid_size)):]

    # Function to copy files to a target directory
    def copy_files(files, target_folder, subfolder):
        target_subfolder = os.path.join(target_folder, subfolder)
        if not os.path.exists(target_subfolder):
            os.makedirs(target_subfolder)
        for f in files:
            shutil.copy(os.path.join(source_folder, f), os.path.join(target_subfolder, f))

    # Copy files to their respective folders
    copy_files(train_files, train_folder, 'index')
    copy_files(valid_files, valid_folder, 'index')
    copy_files(test_files, test_folder, 'index')

    print(f"Files distributed: {len(train_files)} to train, {len(valid_files)} to valid, {len(test_files)} to test.")
    
    return train_files, valid_files, test_files

def copy_image_files(train_files, valid_files, test_files, output_folder, image_source_folder):
    def copy_matching_files(files, target_folder):
        target_image_folder = os.path.join(target_folder, 'image')
        if not os.path.exists(target_image_folder):
            os.makedirs(target_image_folder)
        for f in files:
            image_path = os.path.join(image_source_folder, f)
            if os.path.exists(image_path):
                shutil.copy(image_path, os.path.join(target_image_folder, f))

    # Copy matching images to their respective folders
    copy_matching_files(train_files, os.path.join(output_folder, 'train'))
    copy_matching_files(valid_files, os.path.join(output_folder, 'valid'))
    copy_matching_files(test_files, os.path.join(output_folder, 'test'))

    print("Image files copied to respective folders.")

# Define folder paths
source_folder = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\index"
output_folder = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska"
image_source_folder = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\image"

# Call the function to split data
train_files, valid_files, test_files = split_data(source_folder, output_folder)

# Call the function to copy matching image files
copy_image_files(train_files, valid_files, test_files, output_folder, image_source_folder)
