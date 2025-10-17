# -*- coding: utf-8 -*-
"""
Fast Rank Entropy precompute for SAM input (replace Red channel).
- Quantize gray to 32 levels (降噪+提速)
- Rank entropy with circular window (radius=3, ~7x7)
- Reflect padding to avoid border artifacts
- Output uint8 PNG (0..255), same filename to another folder
- Multiprocessing + console progress bar

Author: RF + assistant
"""

import os
import sys
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from skimage import io, color, morphology, filters, util

# ===================== 用户配置 ===================== #
input_folder  = r'D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\image'
output_folder = r'D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\glcm_rank'

# Rank Entropy 参数
quant_levels  = 32       # 灰度量化级数（常用 16~64；32 是稳妥选择）
radius        = 3        # 圆形窗口半径（3 -> 7x7）
max_workers   = 6        # 并行进程数（按CPU核心调整）
# =================================================== #


# ---------- 工具函数 ----------

def convert_seconds_to_hms(seconds: float):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return h, m, s

def format_hms(seconds: float) -> str:
    h, m, s = convert_seconds_to_hms(seconds)
    return f"{h:02d}:{m:02d}:{s:02d}"

def print_progress(done: int, total: int, start_time: float, bar_width: int = 36):
    elapsed = time.time() - start_time
    rate = (done / elapsed) if (elapsed > 0 and done > 0) else 0.0
    remaining = (total - done) / rate if rate > 0 else 0.0
    pct = (done / total) * 100 if total else 0.0

    filled = int(bar_width * done / total) if total else 0
    bar = "█" * filled + "░" * (bar_width - filled)
    msg = (
        f"\r[{bar}] {pct:6.2f}%  "
        f"{done}/{total}  "
        f"Elapsed {format_hms(elapsed)}  "
        f"ETA {format_hms(remaining) if rate>0 else '--:--:--'}"
    )
    sys.stdout.write(msg)
    sys.stdout.flush()

def to_uint8_gray(img) -> np.ndarray:
    """统一把输入转为 0..255 的 uint8 灰度"""
    if img.ndim == 3:
        gray = color.rgb2gray(img)  # 0..1 float
        return (np.clip(gray, 0, 1) * 255.0 + 0.5).astype(np.uint8)
    elif img.ndim == 2:
        if img.dtype == np.uint8:
            return img
        g = img.astype(np.float32)
        g -= g.min()
        denom = g.max() if g.max() > 0 else 1.0
        return (g / denom * 255.0 + 0.5).astype(np.uint8)
    else:
        raise ValueError(f"Unsupported ndim={img.ndim}")

def quantize_to_levels_u8(gray_u8: np.ndarray, levels: int) -> np.ndarray:
    """
    0..255 -> 0..(levels-1) -> 拉回 0..255
    - 先量化可降低噪声和显著提速 rank 直方图统计
    - 再线性拉回到 0..255，满足 rank.entropy 的 uint8 输入要求
    """
    q = (gray_u8.astype(np.uint16) * levels // 256).astype(np.uint8)  # 0..(levels-1)
    if levels <= 1:
        return np.zeros_like(gray_u8, dtype=np.uint8)
    scale = 255 // (levels - 1) if levels > 1 else 255
    return (q.astype(np.uint16) * scale).astype(np.uint8)

def entropy_rank_fast(gray_u8: np.ndarray, levels: int = 32, radius: int = 3) -> np.ndarray:
    """
    Rank Entropy（C 实现，速度快）
    - 先对灰度量化再拉回 0..255（降噪+提速）
    - 使用圆形结构元素（morphology.disk）
    - reflect 填充后再裁回，避免边界伪影
    返回：uint8（0..255），可直接作为 R 通道
    """
    assert gray_u8.dtype == np.uint8

    # 量化并拉回 0..255
    q = quantize_to_levels_u8(gray_u8, levels)

    # reflect 边界填充（避免 rank 默认的边界效应），然后算完裁回
    pad = radius
    qpad = np.pad(q, pad_width=pad, mode='reflect')

    selem = morphology.disk(radius)

    # skimage 版本差异：0.20+ 使用 footprint 参数名；旧版用 selem
    # 这里做个兼容调用：
    try:
        ent_pad = filters.rank.entropy(qpad, footprint=selem)  # 新版
    except TypeError:
        ent_pad = filters.rank.entropy(qpad, selem=selem)      # 旧版

    ent = ent_pad[pad:-pad, pad:-pad] if pad > 0 else ent_pad

    # rank.entropy 返回即为 uint8（0..255），表示 0..log2(num_bins) 的线性映射。
    # 直接返回即可，保持不同影像可比（固定标度）。
    return ent.astype(np.uint8)

# ---------- 处理单张影像 ----------

def process_single_image(filename: str):
    try:
        in_path = os.path.join(input_folder, filename)
        t0 = time.time()

        img = io.imread(in_path)
        if img is None:
            return filename, None, "failed to load"

        gray_u8 = to_uint8_gray(img)

        # 计算 Rank Entropy（uint8, 0..255）
        ent_u8 = entropy_rank_fast(gray_u8, levels=quant_levels, radius=radius)

        # 保存（同名不同文件夹）
        base = os.path.splitext(filename)[0]
        out_path = os.path.join(output_folder, f"{base}.png")
        io.imsave(out_path, ent_u8)

        dt = time.time() - t0
        return filename, dt, None

    except Exception as e:
        return filename, None, str(e)

# ---------- 主流程 ----------

def main():
    os.makedirs(output_folder, exist_ok=True)
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]

    total = len(image_files)
    if total == 0:
        print(f"No PNG images found in {input_folder}.")
        return

    print(f"Found {total} images. method=rank_entropy, levels={quant_levels}, radius={radius}")
    start = time.time()
    done = 0
    # 先画一条空进度条
    print_progress(done, total, start)

    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        fut_map = {ex.submit(process_single_image, f): f for f in image_files}
        for fut in as_completed(fut_map):
            fname = fut_map[fut]
            try:
                filename, dt, err = fut.result()
                done += 1
                # 单条结果输出（换行），随后刷新进度条
                sys.stdout.write("\n")
                if err is None and dt is not None:
                    h, m, s = convert_seconds_to_hms(dt)
                    print(f"[OK] {filename} in {h}h {m}m {s}s")
                else:
                    print(f"[ERR] {filename}: {err}")
            except Exception as e:
                done += 1
                sys.stdout.write("\n")
                print(f"[ERR] {fname}: {e}")

            print_progress(done, total, start)

    sys.stdout.write("\n")
    total_elapsed = time.time() - start
    H, M, S = convert_seconds_to_hms(total_elapsed)
    print(f"\nProcessing complete. {done}/{total} done. Total time {H}h {M}m {S}s.")

if __name__ == "__main__":
    main()
