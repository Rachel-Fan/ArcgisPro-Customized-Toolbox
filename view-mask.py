import numpy as np

# Assuming 'image' is your NumPy array with values in the range of 0 to 1
# Convert the image to 0-255 range by multiplying with 255 and converting to integer
image_255 = (image * 255).astype(np.uint8)