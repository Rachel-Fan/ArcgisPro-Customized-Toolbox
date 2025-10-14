
import os
import re

# === 硬编码路径 ===
ROOT = r"D:\Eelgrass_processed_images_2025\Index_tif\BC"

# 匹配形式：AA_NN_NN后面跟任意字符
# AA = 两位字母（可大小写）
# NN = 两位数字
pattern = re.compile(r'^([A-Za-z]{2})_(\d{2})_(\d{2})(.*)$', re.IGNORECASE)
# 跳过已是 AA_BC_NN... 的文件
already_ok = re.compile(r'^([A-Za-z]{2})_BC_(\d{2})(.*)$', re.IGNORECASE)

renamed = 0
skipped = 0

for dirpath, _, filenames in os.walk(ROOT):
    for name in filenames:
        if already_ok.match(name):
            skipped += 1
            continue

        m = pattern.match(name)
        if not m:
            skipped += 1
            continue

        code = m.group(1).upper()      # 两位字母
        yy_second = m.group(3)         # 第二组数字（保留）
        rest = m.group(4)              # 其余部分（下划线、文字、扩展名）

        new_name = f"{code}_BC_{yy_second}{rest}"
        old_path = os.path.join(dirpath, name)
        new_path = os.path.join(dirpath, new_name)

        if old_path == new_path:
            skipped += 1
            continue

        print(f"Rename: {name}  ->  {new_name}")
        try:
            os.rename(old_path, new_path)
            renamed += 1
        except Exception as e:
            print(f"  ⚠️ Error renaming {name}: {e}")
            skipped += 1

print("✅ Done.")
print(f"Renamed: {renamed}   Skipped: {skipped}")
