# F1 Tyre Strategy Pipeline

## Overview
This project builds an end-to-end data pipeline to analyze Formula 1 tyre strategy and driver performance using Snowflake and dbt.

The pipeline extracts lap-level telemetry data from FastF1, processes it through a Medallion Architecture (Bronze, Silver, Gold), and generates analytics-ready datasets to support race strategy insights.

---

## Problem Statement
Formula 1 teams must make critical decisions such as tyre selection and pit stop timing under uncertainty.

Raw lap data alone is not sufficient. It must be transformed into meaningful metrics such as:
- Tyre degradation
- Driver consistency
- Stint performance

This project simulates a race strategy analytics pipeline that converts raw data into actionable insights.

---

## Architecture
![Architecture](docs/architecture.png)

---

## Pipeline Flow

FastF1 (Python Extraction)  
→ Raw CSV  
→ Snowflake Bronze  
→ dbt (Silver → Gold)  
→ Data Tests  
→ Analytics Output  

---

## Data Layers

### Bronze
- Raw data from FastF1
- Table: F1_ANALYTICS.BRONZE.F1_LAPS_RAW

### Silver
- Cleaned & structured data
- Tables:
  - SILVER_F1_LAPS_CLEAN
  - SILVER_F1_LAPS_FEATURES

### Gold
- Analytics-ready tables
- Tables:
  - GOLD_F1_TYRE_STRATEGY
  - GOLD_F1_DRIVER_PERFORMANCE
  - GOLD_F1_RACE_SUMMARY

---

## How to Run

1. Install dependencies  
pip install -r requirements.txt  

2. Setup environment (.env)  
SNOWFLAKE_USER=...  
SNOWFLAKE_PASSWORD=...  
SNOWFLAKE_ACCOUNT=...  

3. Run pipeline  
python -m pipeline.run_pipeline --year 2023 --gp Monaco --session R  

---

## Sample Results

Example outputs are stored in:
```
results/
```

### Tyre Strategy (Sample)

| RaceYear | GrandPrix | Compound | Stint | Avg Lap Time |
|----------|----------|----------|-------|--------------|
| 2023 | Monaco | HARD | 1 | 72.18 |
| 2023 | Monaco | MEDIUM | 2 | 72.55 |
| 2023 | Monaco | SOFT | 1 | 73.02 |

---

### Driver Performance (Sample)

| RaceYear | GrandPrix | Driver | Avg Lap Time | Std Dev |
|----------|----------|--------|--------------|--------|
| 2023 | Monaco | STR | 72.30 | 0.45 |
| 2023 | Monaco | HAM | 72.60 | 0.52 |
| 2023 | Monaco | VER | 72.10 | 0.48 |

---

### Race Summary (Sample)

| RaceYear | GrandPrix | Compound | Avg Lap Time |
|----------|----------|----------|--------------|
| 2023 | Monaco | HARD | 72.18 |
| 2023 | Monaco | MEDIUM | 72.55 |
| 2023 | Monaco | SOFT | 73.02 |

---

## How to Use Gold Data

### 1. Dashboard (Streamlit)
Build interactive dashboards to visualize:
- Lap time trends
- Tyre performance
- Driver comparison

### 2. Tyre Degradation Curve
Model how lap time increases over stint length to estimate degradation.

### 3. Pit Stop Recommendation
Use stint + degradation to estimate optimal pit stop timing.

---

## Sample Uses

Example implementations are stored in:
```
sample-uses/
```

Possible extensions:
- Streamlit dashboard app
- Tyre degradation modeling
- Strategy recommendation engine

---

## Tech Stack
- Python (FastF1, Pandas)
- Snowflake
- dbt
- SQL

---

## Future Improvements
- Incremental pipeline
- Multi-race support
- Real-time ingestion
- Advanced ML models
