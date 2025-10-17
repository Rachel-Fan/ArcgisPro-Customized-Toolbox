# -*- coding: utf-8 -*-
import os
import sys
import time
import math
import numpy as np
from skimage import io, color
from skimage.feature import graycomatrix
from concurrent.futures import ProcessPoolExecutor, as_completed

# ===================== 用户配置 ===================== #
input_folder   = r'D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\image'
output_folder  = r'D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\glcm-cpu'

# GLCM 参数（可按需调整）
distances      = [1, 3]                               # 多个像素对距离
angles         = [0, np.pi/4, np.pi/2, 3*np.pi/4]     # 0°,45°,90°,135°
quant_levels   = 16                                   # 灰度量化级数（8~32 较稳）
window_radius  = 7                                    # 滑窗半径；7 -> 15x15 窗口
stride         = 2                                    # 位置步长；1=逐像素，更慢；>1 更快
save_as_tiff   = True                                 # True: 保存 .tif(float32)；False: 保存 .png(uint8缩放)
max_workers    = 4                                    # 并行进程数（建议=物理核数或略小）
EXPECTED_SEC_PER_IMAGE = 107                          # 预估每张耗时，用于初始 ETA
# =================================================== #

# 固定上限（用于 PNG 可视化缩放；PNG 时使用）
HMAX = float(2 * np.log2(quant_levels))               # 例如 levels=16 -> 8.0

# ============== 小工具：时间/进度条/断点续跑判断 ============== #
def convert_seconds_to_hms(seconds: float):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return h, m, s

def format_hms(seconds: float) -> str:
    h, m, s = convert_seconds_to_hms(seconds)
    return f"{h:02d}:{m:02d}:{s:02d}"

def print_progress_line(done, total, start_time, use_observed_avg, expected_spm=EXPECTED_SEC_PER_IMAGE):
    elapsed = time.time() - start_time
    pct = (done / total) if total else 0.0
    if use_observed_avg and done > 0:
        avg = elapsed / done
        eta = (total - done) * avg
    else:
        eta = (total - done) * expected_spm

    bar_width = 30
    filled = int(bar_width * pct)
    bar = "█" * filled + "░" * (bar_width - filled)

    msg = (f"\r[{bar}] {pct*100:6.2f}%  {done}/{total}  "
           f"Elapsed {format_hms(elapsed)}  ETA {format_hms(eta)}")
    sys.stdout.write(msg)
    sys.stdout.flush()

def needs_processing(in_filename: str) -> bool:
    """输出不存在或为空时需要处理；支持断点续跑。"""
    base = os.path.splitext(in_filename)[0]
    out_ext = ".tif" if save_as_tiff else ".png"
    out_path = os.path.join(output_folder, base + out_ext)
    return (not os.path.exists(out_path)) or (os.path.getsize(out_path) == 0)

# ===================== 核心计算函数 ===================== #
def quantize_image_uint8_to_levels(img_uint8: np.ndarray, levels: int) -> np.ndarray:
    """0..255 的 uint8 灰度量化到 0..(levels-1) 的整数。"""
    return (img_uint8.astype(np.uint16) * levels // 256).astype(np.uint8)

def glcm_entropy_avg(window_q: np.ndarray, distances, angles, levels: int) -> float:
    """
    对一个窗口计算 GLCM，并在所有角度/距离上取平均熵（base-2）。
    使用正确的零概率处理（只对 p>0 求 -Σ p log2 p）。
    """
    glcm = graycomatrix(
        window_q, distances=distances, angles=angles,
        levels=levels, symmetric=True, normed=True
    )  # 形状: (levels, levels, len(distances), len(angles))

    H_sum = 0.0
    count = 0
    for di in range(len(distances)):
        for ai in range(len(angles)):
            P = glcm[:, :, di, ai]
            p = P[P > 0]
            if p.size:
                H_sum += -np.sum(p * np.log2(p))
                count += 1
    return (H_sum / max(count, 1))

def compute_glcm_entropy_image(image_uint8: np.ndarray,
                               distances, angles,
                               levels: int = 16,
                               stride: int = 1,
                               window_radius: int = 7) -> np.ndarray:
    """
    整图计算：先量化，再用给定半径窗口逐点/稀疏点计算熵，最后（若 stride>1）用最近邻上采样回原尺寸。
    """
    # 量化到 0..levels-1
    quant = quantize_image_uint8_to_levels(image_uint8, levels)

    H, W = quant.shape
    pad = window_radius
    qpad = np.pad(quant, pad_width=pad, mode='reflect')

    out_h = math.ceil(H / stride)
    out_w = math.ceil(W / stride)
    entropy_sparse = np.zeros((out_h, out_w), dtype=np.float32)

    for ri in range(out_h):
        i = min(ri * stride, H - 1)
        wi = i + pad
        for rj in range(out_w):
            j = min(rj * stride, W - 1)
            wj = j + pad
            window = qpad[wi - window_radius: wi + window_radius + 1,
                          wj - window_radius: wj + window_radius + 1]
            entropy_sparse[ri, rj] = glcm_entropy_avg(window, distances, angles, levels)

    if stride == 1:
        return entropy_sparse[:H, :W]
    else:
        # 最近邻上采样回原尺寸
        ent_full = np.repeat(np.repeat(entropy_sparse, stride, axis=0), stride, axis=1)
        return ent_full[:H, :W]

# ===================== 单图处理（顶层函数，可被多进程pickle） ===================== #
def process_single_image(filename: str):
    try:
        image_path = os.path.join(input_folder, filename)
        t0 = time.time()

        # 读图 & 转灰度（统一到 0..255 的 uint8）
        img = io.imread(image_path)
        if img is None:
            return filename, None, "failed to load"

        if img.ndim == 3:
            gray = color.rgb2gray(img)  # 0..1 float
            gray_uint8 = (np.clip(gray, 0, 1) * 255).astype(np.uint8)
        elif img.ndim == 2:
            if img.dtype != np.uint8:
                g = img.astype(np.float32)
                g -= g.min()
                denom = g.max() if g.max() > 0 else 1.0
                gray_uint8 = (g / denom * 255.0).astype(np.uint8)
            else:
                gray_uint8 = img
        else:
            return filename, None, f"unsupported ndim={img.ndim}"

        # 计算 GLCM 熵图（float32）
        entropy_img = compute_glcm_entropy_image(
            gray_uint8,
            distances=distances, angles=angles,
            levels=quant_levels, stride=stride,
            window_radius=window_radius
        )

        # —— 原子保存（.part → 最终）——
        base = os.path.splitext(filename)[0]
        if save_as_tiff:
            final_path = os.path.join(output_folder, f"{base}.tif")
            tmp_path   = final_path + ".part"
            io.imsave(tmp_path, entropy_img.astype(np.float32))
            os.replace(tmp_path, final_path)  # 原子替换
        else:
            final_path = os.path.join(output_folder, f"{base}.png")
            tmp_path   = final_path + ".part"
            e = np.nan_to_num(entropy_img.astype(np.float32), nan=0.0, posinf=0.0, neginf=0.0)
            e = np.clip(e, 0.0, HMAX)
            e_uint8 = np.round((e / HMAX) * 255.0).astype(np.uint8)
            io.imsave(tmp_path, e_uint8)
            os.replace(tmp_path, final_path)  # 原子替换

        dt = time.time() - t0
        return filename, dt, None

    except Exception as e:
        return filename, None, str(e)

# ===================== 批处理（断点续跑 + 进度 + ETA） ===================== #
def process_images():
    os.makedirs(output_folder, exist_ok=True)

    # 所有输入
    all_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]
    total_all = len(all_files)
    if total_all == 0:
        print(f"No PNG images found in {input_folder}.")
        return

    # 仅处理“尚未完成”的文件（断点续跑）
    image_files = [f for f in all_files if needs_processing(f)]
    total_pending = len(image_files)

    print(f"Found {total_all} images; pending {total_pending} not done yet. "
          f"distances={distances}, angles={len(angles)}, levels={quant_levels}, "
          f"stride={stride}, window_radius={window_radius}, save_as_tiff={save_as_tiff}")
    if total_pending == 0:
        print("Nothing to do. All outputs already exist and are non-empty.")
        return

    # 预估整批 ETA（用你给的每张预计时长）
    total_eta_guess = total_pending * EXPECTED_SEC_PER_IMAGE
    print(f"Estimated time for pending set ({total_pending}): {format_hms(total_eta_guess)}")

    start_time = time.time()
    done = 0

    # 先打印一条进度行（前几张用固定预估；跑几张后切换为实测均值）
    print_progress_line(done, total_pending, start_time, use_observed_avg=False)

    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        fut_map = {ex.submit(process_single_image, f): f for f in image_files}
        switch_after = max(1, min(10, total_pending // 50))  # 1~10 张后切换为“实测均值 ETA”

        for fut in as_completed(fut_map):
            fname = fut_map[fut]
            try:
                filename, dt, err = fut.result()
                done += 1
                sys.stdout.write("\n")
                if err is None and dt is not None:
                    h, m, s = convert_seconds_to_hms(dt)
                    print(f"[OK] {filename} in {h}h {m}m {s}s   ({done}/{total_pending})")
                else:
                    print(f"[ERR] {filename}: {err}          ({done}/{total_pending})")
            except Exception as e:
                done += 1
                sys.stdout.write("\n")
                print(f"[ERR] {fname}: {e}                  ({done}/{total_pending})")

            use_observed = (done >= switch_after)
            print_progress_line(done, total_pending, start_time, use_observed_avg=use_observed)

    sys.stdout.write("\n")
    elapsed = time.time() - start_time
    print(f"\nProcessing complete. {done}/{total_pending} pending files done in {format_hms(elapsed)}.")

# ===================== 入口 ===================== #
if __name__ == "__main__":
    process_images()
