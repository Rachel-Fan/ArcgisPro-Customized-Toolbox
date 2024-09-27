from PIL import Image

# Load the image
image_path  = r"D:\ML_Seagrass\SourceData\Alaska\Alaska\predicted\FI_AK_19_row2_col5.png"
img = Image.open(image_path)

# Convert the image to RGBA format if it is not already
img = img.convert('RGBA')

'''
# Access pixel data
width, height = img.size
pixels = img.load()  # Create a pixel access object

# Print non-black pixel data
for y in range(height):
    for x in range(width):
        # Get RGBA values of the pixel at position (x, y)
        pixel = pixels[x, y]
        if pixel != (0, 0, 0, 255):  # Check if pixel is not all black
            print(f"Pixel at ({x}, {y}): {pixel}")
'''

# Access pixel data
width, height = img.size
pixels = img.load()  # Create a pixel access object

# Initialize counters
black_pixels = 0
non_black_pixels = 0

# Count black and non-black pixels
for y in range(height):
    for x in range(width):
        # Get RGBA values of the pixel at position (x, y)
        pixel = pixels[x, y]
        if pixel == (0, 0, 0, 255):
            black_pixels += 1
        else:
            non_black_pixels += 1

# Print the counts
print(f"Number of black pixels: {black_pixels}")
print(f"Number of non-black pixels: {non_black_pixels}")