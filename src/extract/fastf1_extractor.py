import fastf1
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

CACHE_DIR = BASE_DIR / "cache"
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = RAW_DIR / "laps.csv"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

fastf1.Cache.enable_cache(str(CACHE_DIR))

session = fastf1.get_session(2023, "Monaco", "R")
session.load()

laps = session.laps[["Driver", "LapNumber", "LapTime", "Compound", "Stint"]].copy()

laps.loc[:, "LapTime"] = laps["LapTime"].dt.total_seconds()

laps.to_csv(OUTPUT_FILE, index=False)

print(f"Data saved to {OUTPUT_FILE}")