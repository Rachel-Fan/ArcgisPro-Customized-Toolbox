import os
from collections import defaultdict

def count_images_by_prefix(directory):
    # Dictionary to store counts of images by prefix
    image_count = defaultdict(int)
    

    # Iterate through all files in the specified directory
    for filename in os.listdir(directory):
        # Check if the file is an image
        if filename.endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
            # Split the filename by underscores
            parts = filename.split('_')
            if len(parts) > 2:
                # Extract the prefix before the third underscore
                prefix = '_'.join(parts[0:3])
                # Increment the count for this prefix
                image_count[prefix] += 1
    
    return image_count

def main():
    # Specify the directory containing the images
    directory = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Canada\index'
    
    # Get the counts of images by prefix
    counts = count_images_by_prefix(directory)
    
    # Print the counts
    for prefix, count in counts.items():
        print(f"{prefix}: {count} images")

if __name__ == "__main__":
    main()
