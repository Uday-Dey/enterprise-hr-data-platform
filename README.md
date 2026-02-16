# Enterprise HR Data Platform

This project simulates a production-grade HR data engineering platform
using incremental loading, raw audit history, and curated current-state tables.

## Architecture

Raw HR Files → Incremental ETL → Raw History Table → Current Curated Table

## Tech Stack

- Python
- DuckDB (BigQuery-style warehouse simulation)
- Incremental Timestamp-based Loading
- Git (Enterprise Branching Strategy)
