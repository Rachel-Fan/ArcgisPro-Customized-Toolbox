import os
from PIL import Image
import numpy as np

def collect_unique_colors(folder):
    unique_colors = set()

    for filename in os.listdir(folder):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(folder, filename)
            img = Image.open(image_path).convert("RGB")
            pixels = np.array(img).reshape(-1, 3)

            for pixel in pixels:
                unique_colors.add(tuple(pixel))

    print(f"Total unique colors: {len(unique_colors)}\n")
    for color in sorted(unique_colors):
        print(color)

if __name__ == "__main__":
    input_folder = r"\\wsl.localhost\Ubuntu\home\geofly\sam-hq\train\pa-sam-ggb\Alaska-2025\visualize-0522"

    collect_unique_colors(input_folder)
