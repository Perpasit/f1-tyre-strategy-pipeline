import os
from pathlib import Path

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv


def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "F1_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "F1_ANALYTICS"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    )


def export_table(query: str, output_path: Path):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query)
        df = cur.fetch_pandas_all()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

        print(f"Saved: {output_path}")

    finally:
        cur.close()
        conn.close()


def main():
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env")

    results_dir = root / "results"

    # 1. Tyre Strategy
    export_table(
        """
        SELECT *
        FROM F1_ANALYTICS.PUBLIC_GOLD.GOLD_F1_TYRE_STRATEGY
        ORDER BY raceyear, grandprix
        """,
        results_dir / "tyre_strategy_sample.csv"
    )

    # 2. Driver Performance
    export_table(
        """
        SELECT *
        FROM F1_ANALYTICS.PUBLIC_GOLD.GOLD_F1_DRIVER_PERFORMANCE
        ORDER BY raceyear, grandprix
        """,
        results_dir / "driver_performance_sample.csv"
    )

    # 3. Race Summary
    export_table(
        """
        SELECT *
        FROM F1_ANALYTICS.PUBLIC_GOLD.GOLD_F1_RACE_SUMMARY
        ORDER BY raceyear, grandprix
        """,
        results_dir / "race_summary_sample.csv"
    )


if __name__ == "__main__":
    main()