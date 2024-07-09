import os
import shutil
import random

def split_data(source_folder, train_folder, valid_folder, test_folder, train_size=0.7, valid_size=0.2):
    # Ensure the randomness is reproducible
    random.seed(42)
    
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"The source folder {source_folder} does not exist.")
        return
    
    # Get all files in the source folder
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    random.shuffle(files)
    
    # Split files into train, valid, test according to specified sizes
    total_files = len(files)
    train_files = files[:int(total_files * train_size)]
    valid_files = files[int(total_files * train_size):int(total_files * (train_size + valid_size))]
    test_files = files[int(total_files * (train_size + valid_size)):]

    # Function to copy files to a target directory
    def copy_files(files, target_folder):
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        for f in files:
            shutil.copy(os.path.join(source_folder, f), os.path.join(target_folder, f))

    # Copy files to their respective folders
    copy_files(train_files, train_folder)
    copy_files(valid_files, valid_folder)
    copy_files(test_files, test_folder)

    print(f"Files distributed: {len(train_files)} to train, {len(valid_files)} to valid, {len(test_files)} to test.")

# Define folder paths
source_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All\index"
train_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All\train\index"
valid_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All\valid\index"
test_folder = r"C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All\test\index"

# Call the function
split_data(source_folder, train_folder, valid_folder, test_folder)
