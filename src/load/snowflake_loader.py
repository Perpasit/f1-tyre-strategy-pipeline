import os
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv


# Load environment variables from project root .env
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or str(value).strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def load_csv_to_bronze(csv_path: str) -> None:
    csv_file = Path(csv_path).resolve()

    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    user = _get_env("SNOWFLAKE_USER")
    password = _get_env("SNOWFLAKE_PASSWORD")
    account = _get_env("SNOWFLAKE_ACCOUNT")
    warehouse = _get_env("SNOWFLAKE_WAREHOUSE", "F1_WH")
    database = _get_env("SNOWFLAKE_DATABASE", "F1_ANALYTICS")
    schema = _get_env("SNOWFLAKE_SCHEMA", "BRONZE")
    role = _get_env("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
    )

    cur = conn.cursor()

    try:
        cur.execute(f"USE WAREHOUSE {warehouse}")
        cur.execute(f"USE DATABASE {database}")
        cur.execute(f"USE SCHEMA {schema}")

        cur.execute("""
            CREATE OR REPLACE FILE FORMAT F1_CSV_FORMAT
            TYPE = CSV
            SKIP_HEADER = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        """)

        cur.execute("""
            CREATE OR REPLACE STAGE F1_LAPS_STAGE
            FILE_FORMAT = F1_CSV_FORMAT
        """)

        # Demo-friendly behavior: replace current raw data each run
        cur.execute("TRUNCATE TABLE F1_LAPS_RAW")

        put_sql = f"PUT file://{csv_file.as_posix()} @F1_LAPS_STAGE AUTO_COMPRESS=TRUE OVERWRITE=TRUE"
        cur.execute(put_sql)

        cur.execute("""
            COPY INTO F1_LAPS_RAW
            (RACEYEAR, GRANDPRIX, SESSIONTYPE, DRIVER, LAPNUMBER, LAPTIME, COMPOUND, STINT)
            FROM @F1_LAPS_STAGE
            FILE_FORMAT = (
                TYPE = CSV
                SKIP_HEADER = 1
                FIELD_OPTIONALLY_ENCLOSED_BY = '"'
            )
            ON_ERROR = 'ABORT_STATEMENT'
        """)

        print(f"Loaded CSV into {database}.{schema}.F1_LAPS_RAW from {csv_file}")

    finally:
        cur.close()
        conn.close()