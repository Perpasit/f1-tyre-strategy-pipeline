# Project Title

F1 Tyre Strategy & Race Performance Analytics Pipeline (Snowflake)

# Background & Motivation

Formula 1 is a data-driven sport where race outcomes are heavily influenced by strategic decisions such as tyre selection and pit stop timing. These decisions are often made under uncertainty, relying on historical race data, driver performance, and track conditions.

As a Formula 1 enthusiast, I am interested in understanding how teams decide when to pit and which tyre compounds to use. This project aims to simulate the role of a race strategy analyst by building a data pipeline that transforms raw race data into actionable insights for pre-race planning.

# Objective

The objective of this project is to build an end-to-end data pipeline that converts raw Formula 1 telemetry and race data into analytics-ready datasets that support decision-making for race strategy, particularly:

- Tyre compound selection
- Pit stop timing
- Stint length optimization
- Driver performance comparison

# Problem Statement

Race strategy decisions in Formula 1 are complex and depend on multiple factors such as tyre degradation, driver pace, and track characteristics. However, raw race data is not directly usable for decision-making.

This project addresses the problem by:

Collecting raw lap-level data
Transforming it into structured formats
Generating insights to support strategic planning before a race

# Data Sources

FastF1 (Python Library)
Provides lap-level race data including:

- Lap times
- Tyre compounds
- Stints
- Driver and session data

# Methodology

1. Data Extraction
   - Extract race data using FastF1
   - Store data in CSV/Parquet format
2. Data Loading (Snowflake)
   - Load raw data into Snowflake (Raw Layer)
3. Data Transformation
   - Clean and standardize data
   - Create structured tables (Staging Layer)
4. Feature Engineering
   - Compute:
     - Stint length
     - Lap time degradation
     - Average lap time per compound
     - Driver performance metrics
5. Data Modeling
   - Design analytics-ready tables (Mart Layer)

# Expected Output

## Analytics Tables

- mart_tyre_strategy
- mart_driver_performance
- mart_race_summary

## Example Insights

- Soft tyres degrade faster after a certain number of laps
- Medium tyres provide more consistent performance
- Some drivers maintain stable pace over longer stints

# Business Value / Impact

This project demonstrates how historical race data can be used to support pre-race strategic planning by:

Identifying optimal tyre strategies
Estimating ideal pit stop windows
Comparing driver and team performance

The system acts as a Decision Support System, enabling data-driven decisions instead of relying solely on intuition.

# Technology Stack

- Python (FastF1, Pandas)
- Snowflake (Data Warehouse)
- SQL (Data Transformation)
- GitHub Actions (CI/CD)