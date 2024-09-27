import os

# Define the folder containing the images
image_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Bodega Bay\glcm'

def rename_images(image_folder):
    # Loop through all files in the folder
    for filename in os.listdir(image_folder):
        # Check if the file is an image (e.g., ends with .png or other image formats)
        if filename.endswith('.png'):
            # Find the position of the last underscore in the filename
            last_underscore_index = filename.rfind('_')

            if last_underscore_index != -1:
                # Create a new filename by removing everything after the last underscore (including the underscore)
                new_filename = filename[:last_underscore_index] + '.png'

                # Construct full old and new file paths
                old_file_path = os.path.join(image_folder, filename)
                new_file_path = os.path.join(image_folder, new_filename)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")

# Call the rename_images function
rename_images(image_folder)
