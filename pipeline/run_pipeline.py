import subprocess
import sys


def run_command(command: list[str]) -> None:
    print("Running:", " ".join(command))
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python src/pipeline/run_pipeline.py <year> <gp> [session]")

    year = sys.argv[1]
    gp = sys.argv[2]
    session = sys.argv[3] if len(sys.argv) > 3 else "R"

    output_file = f"data/raw/{gp.lower().replace(' ', '_')}_{year}_{session.lower()}_laps.csv"

    run_command([
        "python",
        "src/extract/fastf1_extractor.py",
        "--year", year,
        "--gp", gp,
        "--session", session,
        "--output", output_file
    ])

    print("Next step: load CSV into Snowflake and run SQL scripts in order.")


if __name__ == "__main__":
    main()