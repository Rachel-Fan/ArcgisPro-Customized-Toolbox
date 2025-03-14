import cv2
import numpy as np
from PIL import Image
import os

def check_opencv_load(image_path):
    """Attempt to load image with OpenCV and return the image."""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"❌ OpenCV failed to load: {image_path}")
    else:
        print(f"✅ OpenCV loaded image successfully: {image_path}")
        print(f"   - Image shape: {image.shape}")
        print(f"   - Data type: {image.dtype}")
    return image

def check_pil_load(image_path):
    """Attempt to load image with PIL and return as NumPy array."""
    try:
        with Image.open(image_path) as img:
            img_array = np.array(img)
            print(f"✅ PIL loaded image successfully: {image_path}")
            print(f"   - Image size: {img.size} (width x height)")
            print(f"   - Mode: {img.mode}")
        return img_array
    except Exception as e:
        print(f"❌ PIL failed to load: {image_path} - {e}")
        return None

def check_image_size(image_path):
    """Check image size using PIL."""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"❌ Failed to read image size with PIL: {e}")
        return None

def check_nan_inf(image, image_name):
    """Check for NaN or Inf values in the image."""
    if np.isnan(image).any():
        print(f"⚠️ Warning: {image_name} contains NaN values.")
    if np.isinf(image).any():
        print(f"⚠️ Warning: {image_name} contains Inf values.")

def check_channels(image, image_name):
    """Check if the image is grayscale, RGB, or RGBA."""
    if len(image.shape) == 2:
        print(f"✅ {image_name} is grayscale (single-channel).")
    elif len(image.shape) == 3:
        if image.shape[2] == 3:
            print(f"✅ {image_name} is RGB (3-channel).")
        elif image.shape[2] == 4:
            print(f"⚠️ {image_name} is RGBA (4-channel), consider removing the alpha channel.")
        else:
            print(f"⚠️ {image_name} has {image.shape[2]} channels, unexpected format.")

def convert_to_uint8(image, image_name):
    """Convert 16-bit or 32-bit images to 8-bit."""
    if image.dtype == np.uint16:
        print(f"⚠️ {image_name} is 16-bit, converting to 8-bit...")
        return (image / 256).astype(np.uint8)
    elif image.dtype == np.float32:
        print(f"⚠️ {image_name} is 32-bit float, converting to 8-bit...")
        return (image * 255).astype(np.uint8)
    return image

def main(drone_image_path, index_image_path):
    """Run all checks on the given drone and index images."""
    
    print("\n🔍 Checking Drone Image\n" + "="*50)
    drone_size = check_image_size(drone_image_path)
    
    drone_image = check_opencv_load(drone_image_path)
    if drone_image is None:
        print("🟡 Trying PIL instead for the drone image...")
        drone_image = check_pil_load(drone_image_path)
    
    if drone_image is not None:
        check_nan_inf(drone_image, "Drone Image")
        check_channels(drone_image, "Drone Image")
        drone_image = convert_to_uint8(drone_image, "Drone Image")

    print("\n🔍 Checking Index Image\n" + "="*50)
    index_size = check_image_size(index_image_path)

    index_image = check_opencv_load(index_image_path)
    if index_image is None:
        print("🟡 Trying PIL instead for the index image...")
        index_image = check_pil_load(index_image_path)
    
    if index_image is not None:
        check_nan_inf(index_image, "Index Image")
        check_channels(index_image, "Index Image")
        index_image = convert_to_uint8(index_image, "Index Image")

    print("\n📊 **Comparison Results**")
    if drone_size and index_size:
        if drone_size == index_size:
            print("✅ Image dimensions match: Drone and Index images have the same width & height.")
        else:
            print(f"⚠️ Image dimensions mismatch! Drone: {drone_size}, Index: {index_size}")

    print("="*50, "\n")

if __name__ == "__main__":
    # User input for image paths
    drone_image_path = input("Enter the full path of the drone image: ").strip()
    index_image_path = input("Enter the full path of the index image: ").strip()

    if not os.path.exists(drone_image_path):
        print(f"❌ Error: Drone image file not found - {drone_image_path}")
    elif not os.path.exists(index_image_path):
        print(f"❌ Error: Index image file not found - {index_image_path}")
    else:
        main(drone_image_path, index_image_path)
