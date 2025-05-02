import os
import time
import numpy as np
import cupy as cp
from skimage import io, color
from skimage.io import imsave
from tqdm import tqdm
from datetime import datetime

# Configuration
input_folder = r'D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\image'
output_folder = r'D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\glcm'
log_path = r"D:\Eelgrass_processed_images_2025\ModelData\Data_by_image_index\Alaska\glcm_log.txt"


# GLCM settings
distance = 3
levels = 64
window_size = distance * 2 + 1

# Logging

def log_and_print(msg):
    print(msg)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")


def convert_seconds_to_hms(seconds):
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return int(h), int(m), int(s)


def quantize_image(image, levels=64):
    return cp.floor(image.astype(cp.float32) / (256 / levels)).astype(cp.uint8)


def compute_glcm_entropy_patchwise(image, distance=3, levels=64, patch_size=7):
    from cupyx.scipy.ndimage import generic_filter

    def glcm_entropy_func(patch):
        ref = patch[:patch_size]
        nei = patch[distance:patch_size+distance]
        glcm, _, _ = np.histogram2d(ref, nei, bins=levels, range=[[0, levels], [0, levels]])
        glcm = glcm / (np.sum(glcm) + 1e-8)
        nonzero = glcm[glcm > 0]
        return -np.sum(nonzero * np.log2(nonzero))

    patch_len = patch_size + distance
    result = generic_filter(cp.asnumpy(image), glcm_entropy_func, size=(1, patch_len), mode='reflect')
    return result.astype(np.float32)


def process_image(filename, start_time):
    try:
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")

        log_and_print(f"\n▶️ {datetime.now()} Start processing {filename}")
        img_start = time.time()

        image_rgb = io.imread(image_path)
        if image_rgb is None:
            return filename, None, "Image load failed."

        gray = color.rgb2gray(image_rgb)
        gray_uint8 = (gray * 255).astype(np.uint8)
        gray_gpu = cp.asarray(gray_uint8)
        quantized = quantize_image(gray_gpu, levels)

        entropy = compute_glcm_entropy_patchwise(quantized, distance=distance, levels=levels, patch_size=window_size)

        entropy_min = np.min(entropy)
        entropy_max = np.max(entropy)
        log_and_print(f"   Entropy range: min={entropy_min:.4f}, max={entropy_max:.4f}")

        if entropy_max > entropy_min:
            normalized_entropy = ((entropy - entropy_min) / (entropy_max - entropy_min + 1e-8) * 255).astype(np.uint8)
        else:
            normalized_entropy = np.zeros_like(entropy, dtype=np.uint8)

        imsave(output_path, normalized_entropy)

        img_end = time.time()
        h, m, s = convert_seconds_to_hms(img_end - img_start)
        log_and_print(f"✅ {datetime.now()} Finished {filename} in {h}h {m}m {s}s")
        return filename, img_end - img_start, f"{h}h {m}m {s}s"

    except Exception as e:
        log_and_print(f"❌ Error processing {filename}: {e}")
        return filename, None, f"❌ Error processing {filename}: {e}"


def process_all_images():
    os.makedirs(output_folder, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"GLCM GPU vectorized log started at {datetime.now()}\n")

    input_images = [f for f in os.listdir(input_folder) if f.endswith(".png")]
    processed = {os.path.splitext(f)[0] for f in os.listdir(output_folder)}
    to_process = [f for f in input_images if os.path.splitext(f)[0] not in processed]

    total = len(to_process)
    if total == 0:
        log_and_print("✅ All images already processed.")
        return

    log_and_print(f"🚀 Processing {total} images with GLCM per-pixel entropy\n")
    start_time = time.time()

    for idx, filename in enumerate(tqdm(to_process, desc="Processing", ncols=80), 1):
        fname, ptime, msg = process_image(filename, start_time)
        if ptime:
            log_and_print(f"[{idx}/{total}] ✅ {fname} processed in {msg}")
        else:
            log_and_print(f"[{idx}/{total}] ⚠️ {fname} failed. {msg}")

    end_time = time.time()
    h, m, s = convert_seconds_to_hms(end_time - start_time)
    log_and_print(f"\n🏁 All done. Total time: {h}h {m}m {s}s")


if __name__ == "__main__":
    process_all_images()
