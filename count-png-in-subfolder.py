import os

def count_png_images(folder_path):
    # Dictionary to store the number of PNG files in each subfolder
    png_counts = {}

    # Traverse the directory tree
    for root, dirs, files in os.walk(folder_path):
        # Count the number of PNG files in the current directory
        png_count = sum(1 for file in files if file.lower().endswith('.png'))
        
        # Store the count in the dictionary with the folder name as the key
        png_counts[root] = png_count

    return png_counts

# Specify the folder path
folder_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\Data\ModelData\Canada'

# Call the function and get the result
result = count_png_images(folder_path)

# Print the results
for subfolder, count in result.items():
    print(f'{subfolder}: {count} PNG images')
