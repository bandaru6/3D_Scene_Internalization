#!/usr/bin/env python3
from pathlib import Path
import argparse
import cv2
import pandas as pd
import math

def ts_to_frame(ts_sec: float, fps: float, total_frames: int) -> int:
    if pd.isna(ts_sec):
        return 0
    idx = int(round(ts_sec * fps))
    return max(0, min(total_frames - 1, idx))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", type=str, default="", help="Path to MP4 (optional)")
    ap.add_argument("--n", type=int, default=3, help="How many narrations to sample")
    ap.add_argument("--margin", type=float, default=0.0, help="Extra seconds offset before start (>=0)")
    ap.add_argument("--outdir", type=str, default="outputs/frames_by_narration")
    args = ap.parse_args()

    # 1) choose video
    if args.video:
        mp4 = Path(args.video)
    else:
        mp4s = list(Path("data/raw/HD-EPIC").rglob("*.mp4"))
        if not mp4s:
            raise FileNotFoundError("No MP4 found; download a small video first.")
        mp4 = mp4s[0]
    if not mp4.exists():
        raise FileNotFoundError(f"Video not found: {mp4}")

    # infer video_id
    stem = mp4.stem
    video_id = stem.split("_mp4")[0]

    # 2) open video + get FPS/frame count
    cap = cv2.VideoCapture(str(mp4))
    if not cap.isOpened():
        raise RuntimeError(f"OpenCV could not open {mp4}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video: {mp4} | fps={fps:.3f} | frames={total}")

    # 3) load annotations for this video_id
    pkl = Path("data/annotations/narrations-and-action-segments/HD_EPIC_Narrations.pkl")
    if not pkl.exists():
        raise FileNotFoundError(f"Missing {pkl}")
    df = pd.read_pickle(pkl)
    sub = df[df["video_id"] == video_id].copy()
    if sub.empty:
        raise RuntimeError(f"No narrations found for {video_id}. Check your annotations or file naming.")

    # pick the first N narrations
    sub = sub.sort_values("start_timestamp").head(args.n)

    # 4) for each narration, save frames at start / mid / end
    out_dir = Path(args.outdir) / video_id
    out_dir.mkdir(parents=True, exist_ok=True)

    def save_frame(frame_idx: int, tag: str, i: int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        if ok:
            out = out_dir / f"{i:02d}_{tag}_{frame_idx}.png"
            cv2.imwrite(str(out), frame)
            print(f"Saved {out}")

    for i, row in enumerate(sub.itertuples(index=False), 1):
        st = float(getattr(row, "start_timestamp", 0.0) or 0.0)
        et = float(getattr(row, "end_timestamp", st + 0.5))
        st = max(0.0, st - max(0.0, args.margin))
        mid = (st + et) / 2.0 if et > st else st
        s_idx = ts_to_frame(st, fps, total)
        m_idx = ts_to_frame(mid, fps, total)
        e_idx = ts_to_frame(et, fps, total)

        narration = getattr(row, "narration", "")
        print(f"\nNarration {i}: \"{narration}\"")
        print(f"  start={st:.2f}s -> frame {s_idx} | mid={mid:.2f}s -> {m_idx} | end={et:.2f}s -> {e_idx}")

        save_frame(s_idx, "start", i)
        save_frame(m_idx, "mid", i)
        save_frame(e_idx, "end", i)

    cap.release()
    print("\nDone.")

if __name__ == "__main__":
    main()
