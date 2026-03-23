import argparse
import os
import fastf1
import pandas as pd

fastf1.Cache.enable_cache("cache")


def extract_session(year: int, gp: str, session_type: str = "R") -> pd.DataFrame:
    session = fastf1.get_session(year, gp, session_type)
    session.load()

    laps = session.laps[["Driver", "LapNumber", "LapTime", "Compound", "Stint"]].copy()
    laps["LapTime"] = laps["LapTime"].dt.total_seconds()

    laps["RaceYear"] = year
    laps["GrandPrix"] = gp
    laps["SessionType"] = session_type

    laps = laps[
        [
            "RaceYear",
            "GrandPrix",
            "SessionType",
            "Driver",
            "LapNumber",
            "LapTime",
            "Compound",
            "Stint",
        ]
    ]

    return laps


def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract F1 session lap data from FastF1")
    parser.add_argument("--year", type=int, required=True, help="Race year, e.g. 2023")
    parser.add_argument("--gp", type=str, required=True, help="Grand Prix name, e.g. Monaco")
    parser.add_argument("--session", type=str, default="R", help="Session type, default R")
    parser.add_argument(
        "--output",
        type=str,
        default="data/raw/laps.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()

    df = extract_session(args.year, args.gp, args.session)
    save_to_csv(df, args.output)

    print(f"Saved {len(df)} rows to {args.output}")


if __name__ == "__main__":
    main()