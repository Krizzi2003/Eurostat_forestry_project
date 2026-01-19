# Eurostat Forestry Feature Engineering

This project builds a country-year feature table (2021–2022) from Eurostat forestry datasets.
It downloads official Eurostat data, stores it locally and in PostgreSQL, and performs
feature engineering to create a structured dataset suitable for exploratory analysis
and machine learning.

 **Work in progress**  
The feature engineering pipeline and project structure are implemented, while setup
instructions and analytical components are still being refined.

---

## Project structure

- `src/update_eurostat.py`  
  Downloads selected Eurostat datasets using the `eurostat` Python package and stores:
  - raw CSV files in `data/raw/`
  - tables in a local PostgreSQL database

- `src/build_features.py`  
  Builds a country–year feature table by reading source tables from PostgreSQL and
  merging engineered features.

- `src/features.py`  
  Contains feature engineering logic (filtering, aggregation, pivoting, ratios, merges).

- `docs/`  
  Documentation and data dictionaries.

- `data/raw/`  
  Raw Eurostat CSV files (ignored by git).

- `data/processed/`  
  Final processed datasets and feature tables (ignored by git).

---

## Features included (examples)

- **Production features**
  - roundwood
  - fuelwood
  - industrial roundwood (coniferous / non-coniferous)
  - pellets, panels, pulp and paper products

- **Trade features**
  - import share for industrial roundwood
  - import share for sawnwood

- **Ownership structure**
  - private forests share

- **Economic aggregates (million EUR)**
  - `P1` – Output of forestry and connected secondary activities
  - `B1G` – Gross value added of forestry

---

## Data sources

All data is sourced from official **Eurostat forestry datasets**, including:
- roundwood production and removals
- industrial roundwood and sawnwood trade
- ownership structure of forests
- economic aggregates of the forestry sector

---

## Requirements

- Python 3.x
- PostgreSQL (local instance)
- Python packages listed in `requirements.txt`

---

## Setup (in progress)

Detailed setup instructions are still being finalized.

Currently, the project assumes:
- a local PostgreSQL database
- environment variables defined via a `.env` file (e.g. database connection string)
- dependencies installed from `requirements.txt`

---

## Planned analysis (future work)

Once the final feature dataset is completed, it will be used for:
- exploratory data analysis
- dimensionality reduction (e.g. PCA)
- selected machine learning methods for cross-country comparison and pattern discovery
  in forestry production, trade, and economic performance.

---

## Notes

- `.env`, `venv/`, `data/raw/`, and `data/processed/` are excluded from version control.
- The pipeline is designed to be reproducible: raw data can be re-downloaded and
  processed outputs regenerated.
