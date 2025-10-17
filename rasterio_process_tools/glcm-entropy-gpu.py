# -*- coding: utf-8 -*-
import os
import time
import math
import numpy as np
import torch
import torch.nn.functional as F
from skimage import io, color

# ===================== 用户配置 ===================== #
input_folder  = r'D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\image'
output_folder = r'D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\glcm_gpu'

# 纹理/窗口参数
distances     = [1, 3]                                 # 多距离
angles        = [0, np.pi/4, np.pi/2, 3*np.pi/4]       # 多角度
quant_levels  = 16                                     # 灰度量化级数（8~32 更稳）
win_radius    = 3                                      # 窗口半径；=3 -> 7x7
stride        = 2                                      # 位置采样步长（>=1）
save_as_tiff  = True                                   # True: 输出 .tif(float32)；False: 输出 .png(归一)
device        = 'cuda' if torch.cuda.is_available() else 'cpu'
# =================================================== #

def to_uint8_gray(img):
    if img.ndim == 3:
        g = color.rgb2gray(img).astype(np.float32)
        g = np.clip(g, 0, 1)
        return (g * 255.0 + 0.5).astype(np.uint8)
    elif img.ndim == 2:
        if img.dtype == np.uint8:
            return img
        arr = img.astype(np.float32)
        arr -= arr.min()
        denom = arr.max() if arr.max() > 0 else 1.0
        return (arr / denom * 255.0 + 0.5).astype(np.uint8)
    else:
        raise ValueError(f"unsupported ndim={img.ndim}")

def quantize_uint8(img_u8, levels):
    # 0..255 -> 0..(levels-1)
    return (img_u8.astype(np.uint16) * levels // 256).astype(np.uint8)

def shift_tensor(t: torch.Tensor, dy: int, dx: int):
    # t: (1,1,H,W); 边界用反射填充
    pad_top = max(dy, 0)
    pad_bottom = max(-dy, 0)
    pad_left = max(dx, 0)
    pad_right = max(-dx, 0)
    tpad = F.pad(t, (pad_left, pad_right, pad_top, pad_bottom), mode='reflect')
    H, W = t.shape[-2:]
    y0 = pad_top - dy
    x0 = pad_left - dx
    return tpad[:, :, y0:y0+H, x0:x0+W]

def offsets_from_polar(distances, angles):
    # 取最近整数偏移，保证与 skimage 的 (distance, angle) 定义一致
    offs = []
    for d in distances:
        for a in angles:
            dy = int(round(-d * np.sin(a)))  # 图像行向下为正，故取负号
            dx = int(round( d * np.cos(a)))
            if (dy, dx) not in offs:
                offs.append((dy, dx))
    return offs

def glcm_entropy_gpu(gray_u8, levels=16, radius=3, stride=2):
    """
    gray_u8: numpy uint8, HxW
    返回：float32 numpy, HxW（与输入同尺寸；内部下采样后再上采样）
    """
    H, W = gray_u8.shape
    # 量化
    q = quantize_uint8(gray_u8, levels)
    # torch 张量 (1,1,H,W)
    x = torch.from_numpy(q).to(device=device, dtype=torch.long)[None, None, :, :]

    # one-hot: (1, L, H, W)
    X = F.one_hot(x, num_classes=levels).permute(0, 4, 2, 3).float()

    # 卷积核: ones 的窗口 (L,1,kh,kw) + groups=L，做各通道独立求和
    k = 2 * radius + 1
    weight = torch.ones((levels, 1, k, k), device=device, dtype=torch.float32)
    # stride 直接用于下采样
    # padding 交给 reflect 边界，不在 conv 里 pad

    # 预计算 offsets
    offs = offsets_from_polar(distances, angles)

    # 为了节省显存，逐个 offset 处理并累加熵
    entropy_sum = None
    count_offsets = 0

    for (dy, dx) in offs:
        # 邻居 one-hot：先移动原始标签，再 one-hot
        y_shift = shift_tensor(x.float(), dy, dx).long()  # (1,1,H,W) long
        Y = F.one_hot(y_shift, num_classes=levels).permute(0, 4, 2, 3).float()  # (1,L,H,W)

        # 对每个 m（邻居灰度）批处理：
        # 我们要计算 对于每个 m: conv2d( X * Y[:,m: m+1], ones_kernel, stride=stride, groups=L )
        # 这样一次就得到所有 (l, m) 的窗口计数（l 维做了 groups 卷积）
        coocents = []
        for m in range(levels):
            prod = X * Y[:, m:m+1, :, :]             # (1, L, H, W)
            # groups=L: (N=1, C_in=L, H, W) * (C_out=L, C_in/groups=1, k, k)
            cnt = F.conv2d(prod, weight, bias=None, stride=stride, padding=0, groups=levels)
            # cnt: (1, L, H', W')，表示固定 m 下所有 l 的计数
            coocents.append(cnt)
        # 拼成 (1, L, L, H', W')
        C = torch.stack(coocents, dim=2)  # (1, L, L, H', W')

        # 归一化为概率
        # 和 skimage 一样，一般 symmetric=True 会合并 (i,j)/(j,i)，这里我们已经对有向偏移计数；
        # 多个 offset 求均值时会平衡方向性。也可在此对 C 与其转置求和/平均，按需调整。
        sumC = C.sum(dim=(1,2), keepdim=True) + 1e-12
        P = C / sumC  # 概率

        # 熵：-Σ p log2 p
        Hs = -(P * (P.clamp_min(1e-12).log2())).sum(dim=(1,2))  # (1, H', W')

        # 累加（对所有 offset 取平均）
        entropy_sum = Hs if entropy_sum is None else (entropy_sum + Hs)
        count_offsets += 1

    entropy_avg = entropy_sum / max(count_offsets, 1)   # (1, H', W')

    # 上采样回原尺寸（最近邻，对应 stride 取样格）
    out = F.interpolate(entropy_avg, size=(H, W), mode='nearest')[0, 0].detach().float().cpu().numpy()
    return out

def process_one_image(path_in, path_out_base):
    img = io.imread(path_in)
    gray = to_uint8_gray(img)
    t0 = time.time()
    ent = glcm_entropy_gpu(gray, levels=quant_levels, radius=win_radius, stride=stride)
    dt = time.time() - t0

    if not os.path.isdir(os.path.dirname(path_out_base)):
        os.makedirs(os.path.dirname(path_out_base), exist_ok=True)

    if save_as_tiff:
        io.imsave(path_out_base + ".tif", ent.astype(np.float32))
    else:
        # 归一化后存 PNG（显示友好）
        e = ent
        e = e - e.min()
        denom = e.max() if e.max() > 0 else 1.0
        io.imsave(path_out_base + ".png", (e / denom).astype(np.float32))
    return dt

def main():
    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]
    if not files:
        print(f"No PNG images found in {input_folder}")
        return
    print(f"Device: {device} | angles={len(angles)} distances={distances} levels={quant_levels} window={2*win_radius+1} stride={stride}")

    T0 = time.time()
    done = 0
    for f in files:
        dt = process_one_image(os.path.join(input_folder, f),
                               os.path.join(output_folder, os.path.splitext(f)[0]))
        done += 1
        h, m = divmod(int(dt), 3600)
        m, s = divmod(m, 60)
        print(f"[{done}/{len(files)}] {f}  {h}h {m}m {s}s")
    H, M = divmod(int(time.time()-T0), 3600)
    M, S = divmod(M, 60)
    print(f"All done: {done}/{len(files)} | Total {H}h {M}m {S}s")

if __name__ == "__main__":
    main()
