#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse
from pathlib import Path

# 站点映射（大小写不敏感）
SITE_MAP = {
    "blackslanding": "BL",
    "blakelanding": "BL",
    "cambell": "CC",
    "campbell": "CC",
    "cambellcove": "CC",
    "campbellcove": "CC",
    "masonmarina": "MM",
    "millertonpoint": "MP",
    "nickcove": "NC",    # 无 s
    "nickscove": "NC",   # 有 s 的写法也支持
    "westside": "WP",
    "westsidepark": "WP",
}

# 匹配模式（关键改动）：
# BB{yy}_{Site}{...}(GR/GRCL/GROM).{baseext}{suffix}
PATTERN = re.compile(
    r'^BB(?P<year>\d{2})_'
    r'(?P<site>[A-Za-z][A-Za-z0-9_\- ]*)'
    r'.*?'                           # 站点后任意字符
    r'(?:GR(?:OM|CL)?)'              # GR / GROM / GRCL
    r'\.(?P<baseext>[A-Za-z0-9]+)'   # 主扩展
    r'(?P<suffix>(\..+)*)$',         # 多重后缀（含 .xml / .aux 等）
    re.IGNORECASE
)


def normalize_site(s: str) -> str:
    """只保留字母并小写，用于去映射表里找缩写。"""
    return re.sub(r'[^a-zA-Z]', '', s).lower()

def plan_new_name(old_name: str):
    m = PATTERN.match(old_name)
    if not m:
        return None, "不匹配命名模式（跳过）"
    year = m.group("year")
    site_raw = m.group("site")
    baseext = m.group("baseext")  # 保留原始大小写
    suffix = m.group("suffix") or ""

    site_key = normalize_site(site_raw)
    abbr = SITE_MAP.get(site_key)
    if not abbr:
        return None, f"站点未在映射表中：{site_raw}（标准化后 {site_key}）（跳过）"

    new_name = f"{abbr}_BB_{year}_Clip.{baseext}{suffix}"
    return new_name, None

from collections import defaultdict

def run(folder: Path, recursive: bool, apply: bool):
    # 仅处理当前文件夹顶层文件（不递归）
    files = [p for p in folder.iterdir() if p.is_file()]
    total = len(files)

    # 预先规划
    plans = []  # (src_path, new_name, err)
    for p in files:
        new_name, err = plan_new_name(p.name)
        plans.append((p, new_name, err))

    # —— 冲突控制策略 ——————————————————————————————
    # 1) 批内“完全相同的新文件名”（含扩展）=> 第二个及以后直接跳过
    used_targets = set()

    # 2) 使用“改名前”的目录快照，检测磁盘已存在的目标
    #    但如果某个名字恰好是“本批将被重命名的源文件名”，不当作阻塞（避免误判交换/覆盖）
    pre_existing = {p.name for p in files}  # 改名前的所有文件名
    source_names = {p.name for p, _, _ in plans}
    pre_existing_safe = pre_existing - source_names

    renamed = skipped = conflicts = 0

    for src, new_name, err in plans:
        if err or new_name is None:
            print(f"[SKIP] {src.name} -> {err or '不匹配命名模式（跳过）'}")
            skipped += 1
            continue

        # A. 批内完全重复目标（包括扩展名一致）——第二个及之后直接跳过
        if new_name in used_targets:
            print(f"[SKIP] {src.name} -> {new_name} 已被本批其他文件使用（完全同名，跳过）")
            conflicts += 1
            skipped += 1
            continue
        used_targets.add(new_name)

        target = src.with_name(new_name)

        # B. 磁盘上（改名前快照）已存在完全同名目标，判定为真实覆盖风险 → 跳过
        if new_name in pre_existing_safe:
            print(f"[⚠️CONFLICT] {src.name} -> {new_name} 已存在于磁盘（改名前快照），跳过以避免覆盖。")
            conflicts += 1
            skipped += 1
            continue

        # ✅ 不再做“Shapefile 同组基名”冲突检查，允许同基名不同扩展一起改
        #    例如：BL_BB_19_Clip.cpg / .dbf / .prj / .shp / .shx / .shp.xml … 都按序改名

        print(f"[RENAME]{' (dry-run)' if not apply else ''} {src.name} -> {new_name}")
        if apply:
            try:
                src.rename(target)
                renamed += 1
            except Exception as e:
                print(f"[ERROR] 重命名 {src.name} 失败: {e}")
                skipped += 1

    print("\n🧾 汇总：")
    print(f"  共扫描文件: {total}")
    print(f"  ✅ 成功重命名: {renamed}")
    print(f"  ⚠️ 冲突/重复跳过: {conflicts}")
    print(f"  ⏸️ 其他跳过: {skipped - conflicts}")
    if not apply:
        print("\n💡 当前为 dry-run 预览模式，未实际修改文件。确认后使用 --apply 执行。")

def main():
    ap = argparse.ArgumentParser(
        description="批量重命名 GROM 产出文件，保持扩展与多重后缀一致，并按站点缩写规范化。"
    )
    ap.add_argument("folder", help="要处理的文件夹路径")
    ap.add_argument("-r", "--recursive", action="store_true", help="递归子目录")
    ap.add_argument("--apply", action="store_true", help="实际执行（默认仅预览）")
    args = ap.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.exists() or not folder.is_dir():
        print(f"路径无效或不是文件夹：{folder}")
        return

    run(folder, recursive=args.recursive, apply=args.apply)

if __name__ == "__main__":
    main()
