#!/usr/bin/env python3
from pathlib import Path
import argparse
import cv2
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=str, default="", help="Directory containing saved frames from extract_frames_at_narrations")
    ap.add_argument("--out", type=str, default="outputs/contact_sheet.png")
    args = ap.parse_args()

    d = Path(args.dir)
    if not d.exists():
        # Try to guess latest subdir
        cand = list(Path("outputs/frames_by_narration").glob("*"))
        if not cand:
            raise FileNotFoundError("No frames_by_narration dir found.")
        d = max(cand, key=lambda p: p.stat().st_mtime)

    # pick three images (start/mid/end) from the first narration
    imgs = sorted([p for p in d.glob("01_*.png")])
    if len(imgs) < 3:
        # fallback: any three images
        imgs = sorted([p for p in d.glob("*.png")])[:3]
    if not imgs:
        raise FileNotFoundError(f"No PNGs found in {d}")

    mats = [cv2.imread(str(p)) for p in imgs[:3] if p.exists()]
    h = min(m.shape[0] for m in mats)
    mats = [cv2.resize(m, (int(m.shape[1]*h/m.shape[0]), h), interpolation=cv2.INTER_AREA) for m in mats]
    sheet = np.concatenate(mats, axis=1)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), sheet)
    print(f"Saved contact sheet: {out}")

if __name__ == "__main__":
    main()
