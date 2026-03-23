# Project Concept: F1 Tyre Strategy & Race Performance Analytics Pipeline

## Background & Motivation

Formula 1 is a highly data-driven sport where race outcomes depend
heavily on strategic decisions such as tyre selection, pit stop timing,
and stint management.

As a Formula 1 enthusiast, this project aims to explore how historical
race data can be transformed into meaningful insights to support race
strategy decisions. It simulates the role of a race strategy analyst by
building a structured data pipeline for analysis.

------------------------------------------------------------------------

## Objective

The objective of this project is to design and implement an end-to-end
data pipeline that transforms raw Formula 1 telemetry data into
analytics-ready datasets for strategy analysis.

Key goals include: - Tyre compound performance analysis
- Driver consistency evaluation
- Stint behavior understanding
- Supporting data-driven race strategy decisions

------------------------------------------------------------------------

## Problem Statement

Raw lap-level race data is complex, unstructured, and not directly
usable for analysis.

Key challenges: - Data is fragmented and noisy
- No structured format for analytics
- Difficult to derive insights such as tyre degradation or driver
consistency

This project addresses these challenges by: - Extracting raw race data
- Structuring and cleaning the data\
- Transforming it into analytical models

------------------------------------------------------------------------

## Data Source

This project uses:

-   FastF1 --- a Python library for accessing Formula 1 telemetry and
    timing data

Data includes: - Lap times
- Tyre compounds
- Stint information
- Driver and session data

------------------------------------------------------------------------

## Methodology

### 1. Data Extraction

-   Extract lap-level data using FastF1
-   Store data as CSV files

### 2. Data Loading

-   Load raw data into Snowflake (Bronze layer)

### 3. Data Transformation

-   Clean and standardize data using dbt (Silver layer)

### 4. Feature Engineering

-   Compute key metrics:
    -   Average lap time per compound
    -   Driver consistency (standard deviation)
    -   Stint-level performance

### 5. Data Modeling

-   Build analytics-ready tables (Gold layer) for downstream use

------------------------------------------------------------------------

## Expected Output

### Analytics Tables

-   `GOLD_F1_TYRE_STRATEGY`
-   `GOLD_F1_DRIVER_PERFORMANCE`
-   `GOLD_F1_RACE_SUMMARY`

### Example Insights

-   Hard tyres provide more stable performance
-   Soft tyres show higher degradation over time
-   Certain drivers maintain more consistent lap times

------------------------------------------------------------------------

## Business Value

This project demonstrates how a data pipeline can support
decision-making in a real-world scenario.

Potential applications: 
- Race strategy planning
- Driver performance analysis
- Tyre selection optimization

The system acts as a **decision support layer**, enabling data-driven
insights instead of relying solely on intuition.

------------------------------------------------------------------------

## Technology Stack

-   Python (FastF1, Pandas)
-   Snowflake (Data Warehouse)
-   dbt (Data Transformation)
-   SQL
-   Streamlit (Visualization)
