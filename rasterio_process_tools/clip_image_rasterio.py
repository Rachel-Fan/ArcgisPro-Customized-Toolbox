import os
import numpy as np
import rasterio
from rasterio.windows import Window
from PIL import Image
import time

def extract_prefix(input_raster):
    basename = os.path.basename(input_raster)
    parts = basename.split("_")
    prefix = "_".join(parts[:3])  # Join the first three parts with an underscore
    return prefix

def clip_image(input_image_path, output_folder, tile_size=512, multiply=False):
    with rasterio.open(input_image_path) as src:
        width, height = src.width, src.height
        num_bands = src.count

        # 计算每个方向上的切片数量（允许边缘不足 512）
        num_tiles_x = (width + tile_size - 1) // tile_size
        num_tiles_y = (height + tile_size - 1) // tile_size

        for y in range(num_tiles_y):
            for x in range(num_tiles_x):
                left = x * tile_size
                upper = y * tile_size
                right = min(left + tile_size, width)
                lower = min(upper + tile_size, height)

                window = Window(left, upper, right - left, lower - upper)
                tile = src.read(window=window)

                # 单波段索引图（0-1）可选放大到 0-255
                if multiply and num_bands == 1:
                    tile = (tile * 255.0).clip(0, 255).astype(np.uint8)

                # 保存 PNG
                if num_bands == 1:
                    tile = np.squeeze(tile, axis=0)
                    img = Image.fromarray(tile.astype(np.uint8), mode="L")
                elif num_bands == 4:
                    tile = np.moveaxis(tile, 0, -1)
                    img = Image.fromarray(tile.astype(np.uint8), mode="RGBA")
                else:
                    tile = np.moveaxis(tile, 0, -1)
                    img = Image.fromarray(tile.astype(np.uint8), mode="RGB")

                output_path = os.path.join(
                    output_folder,
                    f"{extract_prefix(input_image_path)}_row{y+1}_col{x+1}.png"
                )
                img.save(output_path, format="PNG")

    print(f"Clipping completed successfully for {input_image_path}.")

def main(input_folder, index_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # 处理航拍影像（每个年份下面通常只有 1 个 tif）
    if os.path.exists(input_folder):
        for input_image_file in os.listdir(input_folder):
            if input_image_file.lower().endswith(('.tif', '.tiff')):
                input_image_path = os.path.join(input_folder, input_image_file)
                print(f"Processing {input_image_path}")
                image_output_folder = os.path.join(output_folder, f"image_{extract_prefix(input_image_path)}")
                os.makedirs(image_output_folder, exist_ok=True)
                clip_image(input_image_path, image_output_folder)
                print(f"{input_image_file} - Drone image has been extracted.")
                print('**********************************')

    # 处理指数图（如果存在）
    if os.path.exists(index_folder):
        for index_image_file in os.listdir(index_folder):
            if index_image_file.lower().endswith(('.tif', '.tiff')):
                print(f"Index image is {index_image_file}")
                index_image_path = os.path.join(index_folder, index_image_file)
                index_prefix = extract_prefix(index_image_path)
                index_output_folder = os.path.join(output_folder, f"index_{index_prefix}")
                os.makedirs(index_output_folder, exist_ok=True)
                clip_image(index_image_path, index_output_folder, multiply=True)
                print(f"{index_image_file} - Index image is extracted.")
                print('**********************************')

if __name__ == "__main__":
    start_time = time.time()

    # ====== 这里设置你的新的“区域主文件夹”（其下直接是多个 site 子文件夹）======
    # 例如：D:\Eelgrass_Classified_from_Metashape\UTM\Alaska
    region_root = r"D:\Eelgrass_Classified_from_Metashape\UTM\Washington"
    years = ["2019", "2020", "2021", "2022", "2024"]

    # 自动取区域名（用于拼接输出与 index 路径）
    region_name = os.path.basename(os.path.normpath(region_root))

    if not os.path.isdir(region_root):
        raise RuntimeError(f"Region folder not found: {region_root}")

    # 遍历所有站点（site）
    sites = [d for d in os.listdir(region_root) if os.path.isdir(os.path.join(region_root, d))]
    if not sites:
        print(f"No site subfolders found under {region_root}")

    for site in sites:
        site_path = os.path.join(region_root, site)
        print(f"\n===== Site: {site} =====")

        for year in years:
            # 新结构：{region_root}\{site}\{year}\*.tif
            input_folder = os.path.join(site_path, year)

            # 指数图（如果存在）：D:\Eelgrass_processed_images_2025\ModelData\{region}\{site}\{year}\index_tif
            index_folder = os.path.join(
                r"D:\Eelgrass_processed_images_2025\ModelData\Washington_Index", year, "index_tif"
            )

            # 输出：D:\Eelgrass_processed_images_2025\ModelData\Data\{region}\{year}
            output_folder = os.path.join(
                r"D:\Eelgrass_processed_images_2025", "ModelData", "Data", region_name, year
            )

            # 该年份文件夹必须存在且至少包含一个 tif
            has_tif = os.path.isdir(input_folder) and any(
                f.lower().endswith(('.tif', '.tiff')) for f in os.listdir(input_folder)
            )

            if has_tif:
                print(f"Processing {input_folder} (site={site}, year={year})")
                main(input_folder, index_folder, output_folder)
            else:
                print(f"[Skip] No TIFF found for {site} {year}: {input_folder}")

    print('\nAll images have been processed for all sites and years.')

    # 友好的用时输出（自动跳过为 0 的单位，并做单复数处理）
    elapsed = int(time.time() - start_time)
    h, rem = divmod(elapsed, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if h > 0: parts.append(f"{h} hour" + ("s" if h != 1 else ""))
    if m > 0: parts.append(f"{m} minute" + ("s" if m != 1 else ""))
    if s > 0 or not parts: parts.append(f"{s} second" + ("s" if s != 1 else ""))
    print("Execution time: " + " ".join(parts))

'''
if __name__ == "__main__":
    years = ["2019", "2020", "2021", "2022"]
    state = "Alaska"
    
    for year in years:
        print(f"Starting processing for the year {year}")
        
        input_folder = f"D:\\Eelgrass_Classified_from_Metashape\\UTM\\DroneImageByYear\\{state}\\{year}"
        index_folder = f"D:\\Eelgrass_processed_images_2025\\ModelData\\{state}\\{year}\\index_tif"
        output_folder = f"D:\\Eelgrass_processed_images_2025\\ModelData\\Data\\{state}\\{year}"
        
        main(input_folder, index_folder, output_folder)
        
    print('All images have been processed for all years.')
'''