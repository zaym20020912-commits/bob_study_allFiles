from pathlib import Path
import shutil

BASE = Path(r"C:\Users\76710\Desktop\REIT6811\6811Github\bob_study_allFiles\Generative_AI_Research_49805978")
TARGETS = [
    BASE / "Additional Materials",
    BASE / "Drafts and Reports",
    BASE / "Literature Review",
    BASE / "Qualitative Analysis",
    BASE / "Quantitative Analysis",
]

def unique_dest(dst_dir: Path, src_name: str) -> Path:
    dst = dst_dir / src_name
    i = 1
    while dst.exists():
        dst = dst_dir / f"{Path(src_name).stem}({i}){Path(src_name).suffix}"
        i += 1
    return dst

def main():
    moved = 0
    for folder in TARGETS:
        if not folder.exists():
            continue
        for f in folder.rglob("*"):
            if f.is_file():
                dst = unique_dest(BASE, f.name)
                shutil.move(str(f), str(dst))
                moved += 1
    print(f"Restored {moved} files back to base: {BASE}")

if __name__ == "__main__":
    main()
