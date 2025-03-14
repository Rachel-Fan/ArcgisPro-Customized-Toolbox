import os
import numpy as np
from PIL import Image
import rasterio
import tifffile as tiff

# Remove PIL's image size limit
Image.MAX_IMAGE_PIXELS = None  

def check_rasterio_load(image_path):
    """Attempt to load large TIFF using rasterio."""
    try:
        with rasterio.open(image_path) as img:
            print(f"✅ Rasterio loaded image successfully: {image_path}")
            print(f"   - Image size: {img.width} x {img.height}")
            print(f"   - Number of bands: {img.count}")
        return img
    except Exception as e:
        print(f"❌ Rasterio failed to load: {image_path} - {e}")
        return None

def check_tifffile_load(image_path):
    """Attempt to load large TIFF using tifffile."""
    try:
        image = tiff.imread(image_path)
        print(f"✅ tifffile loaded image successfully: {image_path}")
        print(f"   - Image shape: {image.shape}")
        print(f"   - Data type: {image.dtype}")
        return image
    except Exception as e:
        print(f"❌ tifffile failed to load: {image_path} - {e}")
        return None

def main(drone_image_path, index_image_path):
    """Run all checks on the given drone and index images."""
    
    print("\n🔍 Checking Drone Image\n" + "="*50)
    drone_image = check_rasterio_load(drone_image_path) or check_tifffile_load(drone_image_path)
    
    print("\n🔍 Checking Index Image\n" + "="*50)
    index_image = check_rasterio_load(index_image_path) or check_tifffile_load(index_image_path)

if __name__ == "__main__":
    # drone_image_path = input("Enter the full path of the drone image: ").strip()
    # index_image_path = input("Enter the full path of the index image: ").strip()
    
    drone_image_path = r"D:\Eelgrass_Classified_from_Metashape\Test\Alaska\Fishegg\2019\FI_AK_19_UTM8N.tif"
    index_image_path = r"D:\Eelgrass_processed_images_2025\ModelData\Data\ModelData\Alaska_0310_original\2019\Index_tif\FI_AK_19_index_tif.tif"

    if not os.path.exists(drone_image_path):
        print(f"❌ Error: Drone image file not found - {drone_image_path}")
    elif not os.path.exists(index_image_path):
        print(f"❌ Error: Index image file not found - {index_image_path}")
    else:
        main(drone_image_path, index_image_path)
