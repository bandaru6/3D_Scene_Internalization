#!/usr/bin/env python3
from pathlib import Path
import pandas as pd

PKL = Path("data/annotations/narrations-and-action-segments/HD_EPIC_Narrations.pkl")
if not PKL.exists():
    raise FileNotFoundError(f"Missing {PKL}. Did you copy from hd-epic-annotations?")

df = pd.read_pickle(PKL)
print("Columns:", list(df.columns))
print("Total rows:", len(df))

# Infer a video_id from any MP4 you already downloaded
mp4s = list(Path("data/raw/HD-EPIC").rglob("*.mp4"))
if not mp4s:
    raise FileNotFoundError("No MP4 found under data/raw/HD-EPIC.")
mp4 = mp4s[0]
stem = mp4.stem
# Handle names like P01-20240204-130448 or P01-20240204-130448_mp4_to_vrs_time
video_id = stem.split("_mp4")[0]

print(f"Using MP4: {mp4}")
print(f"Inferred video_id: {video_id}")

subset = df[df["video_id"] == video_id].copy()
print(f"Rows for {video_id}: {len(subset)}")
print(subset[["participant_id","video_id","narration","start_timestamp","end_timestamp"]].head(10))

# Save a tiny sample to CSV (for your email / inspection)
out = Path("outputs") / f"{video_id}_narrations_head.csv"
out.parent.mkdir(parents=True, exist_ok=True)
subset.head(50).to_csv(out, index=False)
print(f"Saved sample narrations to {out}")