#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A dumb, name-only classifier:
- Pure substring checks (case-insensitive), no regex, no extension fallback.
- First match wins. If no match, skip the file.
- Recurses the base directory, but skips the 5 target folders.
- Dry-run by default.
"""

from pathlib import Path
import shutil

# ====== 配置 ======
BASE_DIR = Path(r"C:\Users\76710\Desktop\REIT6811\6811Github\bob_study_allFiles\Generative_AI_Research_49805978")
DRY_RUN = False  # 先看计划，确认后改为 False 执行

TARGETS = {
    "qual":       BASE_DIR / "Qualitative Analysis",
    "quant":      BASE_DIR / "Quantitative Analysis",
    "drafts":     BASE_DIR / "Drafts and Reports",
    "literature": BASE_DIR / "Literature Review",
    "additional": BASE_DIR / "Additional Materials",
}

# 仅按名字硬匹配的关键词（小写比较）
KEYWORDS = {
    "qual": [
        "interview", "transcript", "consent", "information sheet", "participant", "ethic",
        "访谈", "逐字稿", "同意书", "信息表", "参与者", "伦理"
    ],
    "quant": [
        "survey", "chart", "comparison", "response", "analysis", "data", "quantitative",
        "问卷", "图表", "对比", "响应", "分析", "数据", "定量"
    ],
    "drafts": [
        "draft", "proposal", "report", "manuscript",
        "草稿", "方案", "报告", "稿件"
    ],
    "literature": [
        "journal", "article", "literature", "ebook", "book", "white paper",
        "文献", "期刊", "书", "白皮书"
    ],
    "additional": [
        "photo", "poster", "slide", "presentation", "diagram", "visual", "media", "brochure", "flyer",
        "照片", "海报", "幻灯", "演示", "示意图", "宣传", "折页", "传单"
    ],
}

# 要跳过的系统文件名（不分类）
SKIP_BASENAMES = {"readme", "license", ".ds_store", "thumbs.db", "desktop.ini"}
# ================


def ensure_dirs():
    for p in TARGETS.values():
        p.mkdir(parents=True, exist_ok=True)


def is_within_targets(path: Path) -> bool:
    pr = path.resolve()
    for t in TARGETS.values():
        if str(pr).startswith(str(t.resolve())):
            return True
    return False


def first_match_category(name_lower: str) -> str | None:
    """
    笨方法：按 KEYWORDS 的顺序遍历，一旦命中某类关键词就返回该类。
    不做优先级融合，不做冲突处理。
    """
    for cat, words in KEYWORDS.items():
        for w in words:
            if w in name_lower:
                return cat
    return None


def iter_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if is_within_targets(p.parent):
            continue
        bn = p.stem.lower()
        if bn in SKIP_BASENAMES:
            continue
        yield p


def unique_dest(dst_dir: Path, filename: str) -> Path:
    dst = dst_dir / filename
    i = 1
    while dst.exists():
        dst = dst_dir / f"{Path(filename).stem}({i}){Path(filename).suffix}"
        i += 1
    return dst


def main():
    if not BASE_DIR.exists():
        raise SystemExit(f"Base directory not found: {BASE_DIR}")

    ensure_dirs()

    total, matched, moved, skipped = 0, 0, 0, 0

    for f in iter_files(BASE_DIR):
        total += 1
        # 名字上下文：仅文件名本身（更笨更直接）；需要也可拼上一级目录名
        name_lower = f.stem.lower()

        cat = first_match_category(name_lower)
        if not cat:
            print(f"[SKIP] {f.relative_to(BASE_DIR)}")
            skipped += 1
            continue

        matched += 1
        dest_dir = TARGETS[cat]
        dest_path = unique_dest(dest_dir, f.name)

        if DRY_RUN:
            print(f"[DRY] {f.relative_to(BASE_DIR)} -> {cat} / {dest_path.name}")
        else:
            shutil.move(str(f), str(dest_path))
            print(f"[OK ] {f.relative_to(BASE_DIR)} -> {cat} / {dest_path.name}")
            moved += 1

    print("\nSummary")
    print(f"- Total files scanned: {total}")
    print(f"- Matched by name:     {matched}")
    print(f"- Skipped (no match):  {skipped}")
    print(f"- Mode:                {'DRY-RUN (no files moved)' if DRY_RUN else f'EXECUTED (moved {moved} files)'}")
    print(f"- Base:                {BASE_DIR}")


if __name__ == "__main__":
    main()
