# -*- coding: utf-8 -*-
"""
Overwrite 4-channel (RGBA) PNGs in-place as 3-channel RGB PNGs.
- Default: drop alpha (fast).
- Optional: composite over white/black/custom background.
- Leaves non-RGBA PNGs untouched.
- Recursive folder walk supported.
- Uses atomic write (.part -> final).

Edit INPUT_ROOT and ALPHA_MODE below, then run.
"""

import os
import numpy as np
from skimage import io

# ======= CONFIG (edit these) =======
INPUT_ROOT     = r"D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\image"
RECURSIVE      = True            # scan subfolders
ALPHA_MODE     = "drop"          # "drop" | "white" | "black" | "custom"
BACKGROUND_RGB = (255, 255, 255) # used when ALPHA_MODE == "custom"
PRINT_EVERY_N  = 500
# ===================================

def list_pngs(root, recursive=True):
    if recursive:
        for dirpath, _, filenames in os.walk(root):
            for f in filenames:
                if f.lower().endswith(".png"):
                    yield os.path.join(dirpath, f)
    else:
        for f in os.listdir(root):
            if f.lower().endswith(".png"):
                yield os.path.join(root, f)

def to_uint8(arr: np.ndarray) -> np.ndarray:
    if arr.dtype == np.uint8:
        return arr
    a = arr.astype(np.float32)
    if a.max() <= 1.0001 and a.min() >= 0.0:  # looks like 0..1
        a = np.clip(a, 0.0, 1.0) * 255.0
    else:
        mn, mx = float(a.min()), float(a.max())
        if mx <= mn:
            a[:] = 0.0
        else:
            a = (a - mn) * (255.0 / (mx - mn))
    return np.clip(a + 0.5, 0, 255).astype(np.uint8)

def composite_over_bg(rgb_u8: np.ndarray, a_u8: np.ndarray, bg_rgb=(255,255,255)) -> np.ndarray:
    if a_u8.ndim == 2:
        a_u8 = a_u8[..., None]
    rgb = rgb_u8.astype(np.float32) / 255.0
    a   = a_u8.astype(np.float32) / 255.0
    bg  = (np.array(bg_rgb, dtype=np.float32)[None, None, :] / 255.0)
    out = rgb * a + bg * (1.0 - a)
    return to_uint8(out)

def overwrite_rgba_with_rgb(path: str) -> bool:
    """Return True if file was converted & overwritten, False if skipped."""
    try:
        arr = io.imread(path)
    except Exception:
        print(f"[ERR] read failed: {path}")
        return False

    # Only touch (H,W,4) images
    if not (arr.ndim == 3 and arr.shape[2] == 4):
        return False

    rgb = to_uint8(arr[..., :3])
    a   = to_uint8(arr[..., 3])

    if ALPHA_MODE == "drop":
        out = rgb
    elif ALPHA_MODE == "white":
        out = composite_over_bg(rgb, a, (255, 255, 255))
    elif ALPHA_MODE == "black":
        out = composite_over_bg(rgb, a, (0, 0, 0))
    else:  # "custom"
        out = composite_over_bg(rgb, a, BACKGROUND_RGB)

    # Atomic write in place
    tmp = path + ".part"
    try:
        io.imsave(tmp, out)
        os.replace(tmp, path)
        return True
    except Exception as e:
        # cleanup temp if needed
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
        print(f"[ERR] write failed: {path} ({e})")
        return False

def main():
    files = list(list_pngs(INPUT_ROOT, RECURSIVE))
    total = len(files)
    print(f"Scanning {total} PNGs under:\n  {INPUT_ROOT}\nMode={ALPHA_MODE}"
          + (f", BG={BACKGROUND_RGB}" if ALPHA_MODE == "custom" else ""))

    converted = 0
    for i, p in enumerate(files, 1):
        changed = overwrite_rgba_with_rgb(p)
        if changed:
            converted += 1
        if i % PRINT_EVERY_N == 0 or i == total:
            print(f"... processed {i}/{total} | converted {converted}")

    print("\n===== Summary =====")
    print(f"Total PNGs     : {total}")
    print(f"RGBA converted : {converted}")
    print("Done. All 4-channel PNGs are now 3-channel RGB in place.")

if __name__ == "__main__":
    main()
