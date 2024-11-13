import os

# Define the folder containing the images
image_folder = r'D:\Seagrass\training_result\glcm_output\pa-sam\Alaska_glcm_pretrained'

def rename_images(image_folder):
    # Loop through all files in the folder
    for filename in os.listdir(image_folder):
        # Check if the file is an image and has the pattern to change (e.g., ends with .png)
        if filename.endswith('.png') and filename.count('.png') > 1:
            # Find the first occurrence of ".png"
            first_png_index = filename.find('.png')

            if first_png_index != -1:
                # Create a new filename by taking everything up to the first ".png"
                new_filename = filename[:first_png_index + 4]

                # Construct full old and new file paths
                old_file_path = os.path.join(image_folder, filename)
                new_file_path = os.path.join(image_folder, new_filename)

                # Rename the file if the new filename is not the same as the old one
                if old_file_path != new_file_path:
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {filename} -> {new_filename}")

# Call the rename_images function
rename_images(image_folder)
