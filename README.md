# Air Quality Exposure Modeling (DC–Baltimore)

## Problem Statement
Fine particulate matter (PM2.5) is a major environmental health risk linked to
cardiopulmonary disease and premature mortality. Observed PM2.5 concentrations
reflect a complex interaction between emissions, meteorology, seasonal variability,
and atmospheric transport.

This project investigates how short-term meteorological conditions modulate
daily PM2.5 exposure patterns across the DC–Baltimore metropolitan corridor
using public ground-based air quality measurements and surface meteorology.

## Scientific Questions
- How does daily PM2.5 variability relate to temperature, wind speed, and humidity?
- Are there seasonal or regime-dependent differences in these relationships?
- Which features dominate interpretable baseline models of PM2.5 exposure?

## Data Sources
- **EPA Air Quality System (AQS):** Daily PM2.5 (FRM/FEM) measurements from
  monitoring stations in Washington, DC, Maryland, and surrounding areas.
- **NOAA Integrated Surface Database (ISD):** Surface meteorological observations
  (temperature, wind speed, relative humidity).

## Methods Overview
- Reproducible data ingestion via scripted downloads
- Daily aggregation and quality control
- Exploratory data analysis and feature engineering
- Interpretable baseline models (e.g., linear models, tree-based models)

## Scope and Constraints
- Focus on daily-aggregated PM2.5 concentrations
- Urban and suburban stations in the DC–Baltimore region
- Emphasis on interpretability rather than complex deep learning models

## Project Structure
- `data/`: raw and processed datasets
- `notebooks/`: exploratory analysis and modeling
- `src/`: data ingestion and preprocessing scripts
- `figures/`: saved plots and figures
- `reports/`: short summaries and notes

All data used in this project are publicly available from the U.S. EPA and NOAA;
see `reports/data_sources.md` for full attribution and provenance details.
