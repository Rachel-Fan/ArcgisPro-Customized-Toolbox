import os

def rename_images(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Check if the file ends with '_0.png' and contains another '.png' earlier in the name
            if file_name.endswith('_0.png') and '.png' in file_name[:-6]:
                # Remove only the '_0.png' and retain the original '.png'
                new_file_name = file_name.replace('_0.png', '')

                # Full paths for the old and new file names
                old_file_path = os.path.join(root, file_name)
                new_file_path = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} -> {new_file_path}')
                
def remove_duplicate_png(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Check if the file name has duplicate '.png'
            if file_name.endswith('.png.png'):
                # Create new file name by replacing '.png.png' with '.png'
                new_file_name = file_name.replace('.png.png', '.png')

                # Full paths for the old and new file names
                old_file_path = os.path.join(root, file_name)
                new_file_path = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} -> {new_file_path}')

# Specify the folder path here
folder_path = r"D:\Seagrass\training_result\glcm_output\pa-sam\Washington"
rename_images(folder_path)
#remove_duplicate_png(folder_path)
