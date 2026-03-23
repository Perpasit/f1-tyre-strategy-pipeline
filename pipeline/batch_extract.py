from src.extract.fastf1_extractor import extract_session, save_to_csv

jobs = [
    (2023, "Monaco", "R"),
    (2023, "Silverstone", "R"),
    (2023, "Mexico City", "R"),
]

for year, gp, session in jobs:
    df = extract_session(year, gp, session)
    output_path = f"data/raw/{gp.lower().replace(' ', '_')}_{year}_{session.lower()}_laps.csv"
    save_to_csv(df, output_path)
    print(f"Saved {output_path}")