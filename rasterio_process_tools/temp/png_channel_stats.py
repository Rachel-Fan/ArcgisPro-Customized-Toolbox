# -*- coding: utf-8 -*-
"""
Hard-coded PNG channel stats:
- Counts 1/3/4/other channels (using skimage.io)
- Prints summary + examples
- Saves optional summary CSV and per-file CSV (each image with channel count)
"""

import os
from collections import defaultdict, Counter
from skimage import io

# ===== CONFIG (edit these) =====
ROOT_FOLDER    = r"D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\image"
RECURSIVE      = True           # scan subfolders
SAMPLE_PER_CL  = 5              # examples to print per class
SUMMARY_CSV    = r"D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\png_channel_stats_summary.csv"   # None to skip
PER_FILE_CSV   = r"D:\Eelgrass_processed_images_2025\ModelData\Data_for_modeling\Washington\png_channels_perfile.csv"        # None to skip
# ==============================

def iter_png_files(root: str, recursive: bool):
    if recursive:
        for dirpath, _, filenames in os.walk(root):
            for f in filenames:
                if f.lower().endswith(".png"):
                    yield os.path.join(dirpath, f)
    else:
        for f in os.listdir(root):
            if f.lower().endswith(".png"):
                yield os.path.join(root, f)

def detect_channels_with_skimage(path: str):
    """
    Return (channels:int, tag:str); read error -> (None, 'ERROR')
    - Gray (H,W) -> (1, 'ndim2-<dtype>')
    - Color (H,W,C) -> (C, 'ndim3-<dtype>')
    - Other -> (-1, 'ndimX-<dtype>')
    """
    try:
        arr = io.imread(path)
    except Exception:
        return None, "ERROR"
    if arr is None:
        return None, "ERROR"
    if arr.ndim == 2:
        return 1, f"ndim2-{arr.dtype}"
    elif arr.ndim == 3:
        return int(arr.shape[2]), f"ndim3-{arr.dtype}"
    else:
        return -1, f"ndim{arr.ndim}-{arr.dtype}"

def main():
    folder = ROOT_FOLDER
    print(f"🔎 Scanning: {folder}")
    if not os.path.isdir(folder):
        print("❌ Folder does not exist. Update ROOT_FOLDER.")
        return

    by_channels = defaultdict(list)   # {1:[paths], 3:[paths], 4:[paths], ...}
    tags = Counter()
    errors = []
    per_file_rows = []                # (path, channels or '', tag)

    total = 0
    for i, path in enumerate(iter_png_files(folder, RECURSIVE), 1):
        ch, tag = detect_channels_with_skimage(path)
        tags[tag] += 1
        if ch is None:
            errors.append(path)
            per_file_rows.append((path, "", tag))
        else:
            by_channels[ch].append(path)
            per_file_rows.append((path, ch, tag))
        total += 1
        if i % 500 == 0:
            print(f"  ... scanned {i} files")

    print("\n================ PNG Channel Statistics ================\n")
    print(f"Root folder    : {os.path.abspath(folder)}")
    print(f"Recursive      : {RECURSIVE}")
    print(f"Total PNG files: {total}")
    print(f"Unreadable     : {len(errors)}\n")

    # order: 1,3,4 then others
    keys = sorted(set(by_channels.keys()))
    for k in (1, 3, 4):
        if k not in keys:
            keys.append(k)
    keys = sorted(set(keys))

    header = f"{'Channels':>8} | {'Count':>8} | {'Percent':>8}"
    print(header)
    print("-" * len(header))
    for ch in keys:
        cnt = len(by_channels.get(ch, []))
        pct = (cnt / total * 100.0) if total else 0.0
        print(f"{str(ch):>8} | {cnt:8d} | {pct:7.2f}%")

    print("\nTags (from skimage):")
    for t, cnt in tags.most_common():
        pct = (cnt / total * 100.0) if total else 0.0
        print(f"  {t:<16} : {cnt:6d}  ({pct:6.2f}%)")

    sample_n = max(0, SAMPLE_PER_CL)
    for ch in keys:
        files = by_channels.get(ch, [])
        if not files:
            continue
        print(f"\nExamples (first {sample_n}) for channels={ch}:")
        for p in files[:sample_n]:
            print("  -", p)

    if errors:
        print(f"\nUnreadable files ({len(errors)}):")
        for p in errors[:sample_n]:
            print("  -", p)
        if len(errors) > sample_n:
            print(f"  ... and {len(errors) - sample_n} more")

    # summary CSV
    if SUMMARY_CSV:
        try:
            import csv
            csv_path = os.path.abspath(SUMMARY_CSV)
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["metric", "value"])
                w.writerow(["root", os.path.abspath(folder)])
                w.writerow(["recursive", RECURSIVE])
                w.writerow(["total_png", total])
                w.writerow(["unreadable", len(errors)])
                for ch in keys:
                    cnt = len(by_channels.get(ch, []))
                    pct = (cnt / total * 100.0) if total else 0.0
                    w.writerow([f"channels_{ch}_count", cnt])
                    w.writerow([f"channels_{ch}_percent", f"{pct:.2f}%"])
                for t, cnt in tags.most_common():
                    pct = (cnt / total * 100.0) if total else 0.0
                    w.writerow([f"tag_{t}_count", cnt])
                    w.writerow([f"tag_{t}_percent", f"{pct:.2f}%"])
            print(f"\n✅ Summary CSV saved: {csv_path}")
        except Exception as e:
            print(f"\n⚠️ Failed to write summary CSV: {e}")

    # per-file CSV
    if PER_FILE_CSV:
        try:
            import csv
            csv_path2 = os.path.abspath(PER_FILE_CSV)
            with open(csv_path2, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["path", "channels", "tag"])
                for row in per_file_rows:
                    w.writerow(row)
            print(f"✅ Per-file CSV saved: {csv_path2}")
        except Exception as e:
            print(f"⚠️ Failed to write per-file CSV: {e}")

    print("\n========================================================\n")

if __name__ == "__main__":
    main()
