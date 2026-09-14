#!/usr/bin/env python3
"""Split a folder of .txt files into N subfolders balanced by total byte size.

Uses greedy bin-packing (Longest Processing Time): files are sorted largest
first, then each is placed in whichever output folder currently holds the
least data. This keeps the total size of the folders close to equal.

(base) sguhr@Svenjas-MacBook-Pro Short_Stories % python equally_sized_folder_split.py
part_1: 100 files,   25.0 MB
part_2: 100 files,   25.0 MB
part_3:  99 files,   25.0 MB
part_4:  99 files,   25.0 MB
part_5:  99 files,   25.0 MB
part_6:  99 files,   25.0 MB

Total: 596 files, 149.9 MB -> /Users/sguhr/Downloads/Short_Story_Files_equally_sized_folders
"""


import shutil
from pathlib import Path

# --- Configuration -----------------------------------------------------------
INPUT_DIR = Path("/Users/sguhr/Downloads/Short_Story_Files_left_for_splitting")
NUM_FOLDERS = 6
OUTPUT_PARENT = INPUT_DIR.parent / "Short_Story_Files_equally_sized_folders"
MOVE = False  # False = copy (non-destructive); True = move originals
# -----------------------------------------------------------------------------


def main():
    files = sorted(
        (p for p in INPUT_DIR.iterdir()
         if p.is_file() and p.suffix.lower() == ".txt"),
        key=lambda p: p.stat().st_size,
        reverse=True,
    )
    if not files:
        raise SystemExit(f"No .txt files found in {INPUT_DIR}")

    bins = [[] for _ in range(NUM_FOLDERS)]
    sizes = [0] * NUM_FOLDERS
    for f in files:
        i = sizes.index(min(sizes))  # currently-smallest folder
        bins[i].append(f)
        sizes[i] += f.stat().st_size

    transfer = shutil.move if MOVE else shutil.copy2
    for idx, (bin_files, total) in enumerate(zip(bins, sizes), start=1):
        dest = OUTPUT_PARENT / f"part_{idx}"
        dest.mkdir(parents=True, exist_ok=True)
        for f in bin_files:
            transfer(str(f), str(dest / f.name))
        print(f"part_{idx}: {len(bin_files):>3} files, {total / 1e6:6.1f} MB")

    print(f"\nTotal: {len(files)} files, {sum(sizes) / 1e6:.1f} MB "
          f"-> {OUTPUT_PARENT}")


if __name__ == "__main__":
    main()