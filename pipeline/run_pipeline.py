import argparse
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.extract.fastf1_extractor import extract_session, save_to_csv
from src.load.snowflake_loader import load_csv_to_bronze


def run_dbt_command(command: list[str], working_dir: Path) -> None:
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, cwd=working_dir, check=False)

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}")


def query_gold_outputs() -> None:
    import os
    import snowflake.connector

    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "F1_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "F1_ANALYTICS"),
        schema=os.getenv("SNOWFLAKE_SCHEMA", "BRONZE"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    )

    cur = conn.cursor()

    try:
        print("\n=== GOLD: Tyre Strategy ===")
        cur.execute("""
            SELECT raceyear, grandprix, compound, stint, avg_laptime
            FROM F1_ANALYTICS.PUBLIC_GOLD.GOLD_F1_TYRE_STRATEGY
            ORDER BY raceyear, grandprix, avg_laptime
            LIMIT 10
        """)
        for row in cur.fetchall():
            print(row)

        print("\n=== GOLD: Driver Performance ===")
        cur.execute("""
            SELECT raceyear, grandprix, driver, avg_laptime, laptime_stddev
            FROM F1_ANALYTICS.PUBLIC_GOLD.GOLD_F1_DRIVER_PERFORMANCE
            ORDER BY raceyear, grandprix, laptime_stddev
            LIMIT 10
        """)
        for row in cur.fetchall():
            print(row)

        print("\n=== GOLD: Race Summary ===")
        cur.execute("""
            SELECT raceyear, grandprix, compound, avg_laptime
            FROM F1_ANALYTICS.PUBLIC_GOLD.GOLD_F1_RACE_SUMMARY
            ORDER BY raceyear, grandprix, avg_laptime
            LIMIT 10
        """)
        for row in cur.fetchall():
            print(row)

    finally:
        cur.close()
        conn.close()


def main() -> None:
    root_dir = Path(__file__).resolve().parents[1]
    load_dotenv(root_dir / ".env")

    parser = argparse.ArgumentParser(description="Run end-to-end F1 tyre strategy pipeline")
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

    dbt_dir = root_dir / "f1_dbt"
    output_path = root_dir / args.output

    print("=== STEP 1: Extract from FastF1 ===")
    df = extract_session(args.year, args.gp, args.session)
    save_to_csv(df, str(output_path))
    print(f"Saved {len(df)} rows to {output_path}")

    print("\n=== STEP 2: Load to Snowflake Bronze ===")
    load_csv_to_bronze(str(output_path))

    print("\n=== STEP 3: Run dbt models ===")
    run_dbt_command(["dbt", "run"], dbt_dir)

    print("\n=== STEP 4: Run dbt tests ===")
    run_dbt_command(["dbt", "test"], dbt_dir)

    print("\n=== STEP 5: Query Gold outputs ===")
    query_gold_outputs()

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nPipeline failed: {exc}", file=sys.stderr)
        sys.exit(1)