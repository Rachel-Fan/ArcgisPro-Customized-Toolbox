import os
import re

# === 硬编码：根目录路径 ===
ROOT = r"D:\Eelgrass_processed_images_2025\ModelData\Data"

# 目标形式：<AA>_BC_<YY>...
ALREADY_OK_RE = re.compile(r'^([A-Za-z]{2})_BC_(\d{2})(.*)$', re.IGNORECASE)

# 原始形式：<AA>_<NN>_<NN><rest>
# 例：DU_19_19_index_tif(XXX).tif、BH_07_07_foo.bar、WA_23_23.tif 等
# 也兼容两组数字不同的情况（例如 DU_18_19_xxx → DU_BC_19_xxx）
PATTERN = re.compile(r'^([A-Za-z]{2})_(\d{2})_(\d{2})(.*)$', re.IGNORECASE)

renamed = 0
skipped = 0

for dirpath, _, filenames in os.walk(ROOT):
    for name in filenames:
        # 已经是 AA_BC_YY... 的跳过
        if ALREADY_OK_RE.match(name):
            skipped += 1
            continue

        m = PATTERN.match(name)
        if not m:
            # 不符合前缀两字母 + 两组两位数字的命名，跳过
            skipped += 1
            continue

        code = m.group(1)            # 两位字母
        yy_second = m.group(3)       # 第二组两位数字（要保留的那个）
        rest = m.group(4)            # 其余部分（含下划线/文字/扩展名等）

        new_name = f"{code.upper()}_BC_{yy_second}{rest}"

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
            print(f"  !! ERROR renaming {name}: {e}")
            skipped += 1

print("✅ Done.")
print(f"Renamed: {renamed}   Skipped: {skipped}")
