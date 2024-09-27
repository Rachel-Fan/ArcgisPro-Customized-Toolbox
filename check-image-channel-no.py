from PIL import Image
import os

def count_rgb_rgba_images(image_folder):
    # List all files in the folder
    files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    
    rgb_count = 0
    rgba_count = 0
    rgba_images = []

    for idx, file in enumerate(files):
        image_path = os.path.join(image_folder, file)
        
        try:
            # Open the image
            with Image.open(image_path) as img:
                # Get the mode of the image
                mode = img.mode
                
                # Count and record based on the mode
                if mode == 'RGB':
                    rgb_count += 1
                elif mode == 'RGBA':
                    rgba_count += 1
                    rgba_images.append(file)
        
        except Exception as e:
            print(f"Error processing {file}: {e}")

    # Print summary
    print(f"Total images processed: {len(files)}")
    print(f"Number of RGB images: {rgb_count}")
    print(f"Number of RGBA images: {rgba_count}")
    
    # List all RGBA images
    if rgba_images:
        print("\nList of RGBA images:")
        for img in rgba_images:
            print(img)
    else:
        print("\nNo RGBA images found.")

if __name__ == "__main__":
    # Specify the folder containing the images
    image_folder = r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Canada\image'
    
    # Count and list RGBA images
    count_rgb_rgba_images(image_folder)
