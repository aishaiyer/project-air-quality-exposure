"""
Merge PM2.5 (EPA AQS) with Meteorology (NOAA ISD-Lite)

Inputs:
- data/processed/pm25_daily_dc_md.csv
- data/processed/meteorology_daily_isd.csv

Output:
- data/processed/modeling_table_pm25_met.csv
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROC_DIR = PROJECT_ROOT / "data" / "processed"

PM25_PATH = PROC_DIR / "pm25_daily_dc_md.csv"
MET_PATH = PROC_DIR / "meteorology_daily_isd.csv"
OUT_PATH = PROC_DIR / "modeling_table_pm25_met.csv"

# Station ID → airport label
STATION_LABELS = {
    "724050-13743": "DCA",
    "724060-93721": "BWI",
    "724030-93738": "IAD",
}

# Simple county → met station mapping (v1)
# You can expand/adjust later; this is a sensible starting point.
COUNTY_TO_STATION = {
    # DC (AQS often reports "District of Columbia" as the county)
    "District of Columbia": "DCA",

    # Maryland — Baltimore region
    "Baltimore": "BWI",
    "Baltimore City": "BWI",
    "Anne Arundel": "BWI",
    "Howard": "BWI",
    "Harford": "BWI",

    # Maryland — DC suburbs
    "Montgomery": "DCA",
    "Prince George's": "DCA",

    # Maryland — western/other (proxy)
    "Frederick": "IAD",
    "Carroll": "IAD",
    "Charles": "DCA",
    "Calvert": "BWI",
    "St. Mary's": "BWI",
}


def load_pm25():
    df = pd.read_csv(PM25_PATH, parse_dates=["date"])
    return df


def load_met():
    met = pd.read_csv(MET_PATH, parse_dates=["date"])

    # station field currently like "724050-13743-2018"
    # Extract the ID prefix "724050-13743"
    met["station_id"] = met["station"].str.split("-").str[0:2].str.join("-")

    # Map to airport label
    met["met_station"] = met["station_id"].map(STATION_LABELS)

    # Keep only DCA/BWI/IAD rows
    met = met[met["met_station"].notna()].copy()
    
    # Ensure uniqueness: one row per (date, met_station)
    # If there are multiple observations per day, aggregate to daily means/sums.
    agg = {
        "temp": "mean",
        "dewpoint": "mean",
        "sea_level_pressure": "mean",
        "wind_speed": "mean",
        "precipitation": "sum",   # precipitation is additive
        "snow_depth": "mean",
    }
    met = met.groupby(["date", "met_station"], as_index=False).agg(agg)

    # Drop original station strings; keep cleaned label
    # met = met.drop(columns=["station", "station_id"])

    return met


def assign_met_station(pm25: pd.DataFrame) -> pd.DataFrame:
    pm25["met_station"] = pm25["County Name"].map(COUNTY_TO_STATION)

    # If any counties are unmapped, fall back:
    # - If state is DC → DCA
    # - else default to DCA (simple; we can improve later)
    pm25.loc[(pm25["met_station"].isna()) & (pm25["State Name"] == "District Of Columbia"), "met_station"] = "DCA"
    pm25.loc[pm25["met_station"].isna(), "met_station"] = "DCA"

    return pm25


def main():
    pm25 = load_pm25()
    met = load_met()

    pm25 = assign_met_station(pm25)
    print("Met key duplicates:", met.duplicated(subset=["date", "met_station"]).sum())

    merged = pm25.merge(
        met,
        how="left",
        on=["date", "met_station"],
        validate="m:1",
    )

    # Basic merge diagnostics
    missing_met = merged["temp"].isna().mean()
    print(f"Merged rows: {len(merged):,}")
    print(f"Fraction missing meteorology (temp): {missing_met:.3f}")
    print("Met stations used:", merged["met_station"].value_counts().to_dict())

    merged.to_csv(OUT_PATH, index=False)
    print(f"Saved modeling table to: {OUT_PATH}")


if __name__ == "__main__":
    main()
