import numpy as np
import matplotlib.pyplot as plt

def visualize_image(image_path):
    # Load the image
    img = plt.imread(image_path)

    # Display the shape of the image to confirm channel information
    print("Image shape:", img.shape)

    # Initialize counters
    black_pixels = 0
    non_black_pixels = 0

    # Create a new RGB image; initially set all pixels to black
    rgb_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    # Iterate over each pixel to apply conditions and count
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            pixel = img[x, y]
            # Check if pixel is black (without considering an alpha channel)
            if np.all(pixel == [0, 0, 0]):
                black_pixels += 1
            else:
                non_black_pixels += 1
                # Set non-black pixels to yellow
                rgb_image[x, y] = [255, 255, 0]  # RGB for yellow

    print(f"Black pixels: {black_pixels}, Non-black pixels: {non_black_pixels}")

    # Display the original image
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(img)
    plt.axis('off')
    
    # Display the modified image
    plt.subplot(1, 2, 2)
    plt.title('Modified Image')
    plt.imshow(rgb_image)
    plt.axis('off')
    
    plt.show()

# Replace the path with the path to your RGB image
visualize_image(r'C:\Users\GeoFly\Documents\rfan\Seagrass\image\Non_Zero\All\train\index\BA_OR_19_tile_117.png')
