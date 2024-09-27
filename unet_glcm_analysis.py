import matplotlib.pyplot as plt
import numpy as np
from skimage import io, color
from skimage.feature import graycomatrix, graycoprops
from skimage.util import view_as_windows

# Load and convert the image to grayscale
image_path = r'C:\Users\GeoFly\Documents\rfan\Seagrass\glcm\images\BA_OR_21_row26_col15.png'
image_rgb = io.imread(image_path)  # Replace with your image path
image_gray = color.rgb2gray(image_rgb)

# Convert grayscale image to uint8
image_gray_uint8 = (image_gray * 255).astype(np.uint8)

def compute_texture_image(image, distances, angles, properties):
    height, width = image.shape
    texture_images = {prop: np.zeros((height, width)) for prop in properties}

    # Define the window size
    window_size = max(distances) * 2 + 1  # Ensuring the window covers the distance

    # Create a padded image
    padded_image = np.pad(image, pad_width=max(distances), mode='constant', constant_values=0)

    for i in range(height):
        for j in range(width):
            print(f'processing i={i}, j={j} ----------------------')
            # Extract the window around the current pixel
            window = padded_image[i:i + window_size, j:j + window_size]

            # Compute the GLCM for the window
            glcm = graycomatrix(window, distances, angles, symmetric=True, normed=True)

            # Compute the texture properties from the GLCM
            for prop in properties:
                texture_images[prop][i, j] = graycoprops(glcm, prop).mean()

    return texture_images


# Define the distance and angle for the GLCM computation
distances = [3]  # Distance between pixel pairs
angles = [1]     # Angle in radians (0 radians corresponds to horizontal direction)
#properties = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation']
properties = ['energy']

# Compute texture images
texture_images = compute_texture_image(image_gray_uint8, distances, angles, properties)


import matplotlib.pyplot as plt

# Display texture images
plt.figure(figsize=(15, 10))

for i, prop in enumerate(properties):
    plt.subplot(1, len(properties), i + 1)
    plt.imshow(texture_images[prop], cmap='gray')
    plt.title(prop)
    plt.axis('off')

plt.show()
#%%
#%%