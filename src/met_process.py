"""
NOAA ISD-Lite Meteorology Processing (TXT files)

- Reads ISD-Lite daily text files
- Parses meteorological variables
- Outputs a clean daily meteorology dataset
"""

from pathlib import Path
import pandas as pd

# Always resolve paths from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "isd_lite"
OUT_DIR = PROJECT_ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ISD-Lite daily column order (fixed)
COLUMNS = [
    "year", "month", "day",
    "temp", "dewpoint",
    "sea_level_pressure",
    "wind_speed",
    "precipitation",
    "snow_depth",
]


def parse_isd_lite_file(path: Path) -> pd.DataFrame:
    rows = []
    with open(path, "r") as f:
        for line in f:
            vals = line.strip().split()
            if len(vals) < len(COLUMNS):
                continue
            rows.append(vals[:len(COLUMNS)])

    if not rows:
        return pd.DataFrame(columns=COLUMNS)

    return pd.DataFrame(rows, columns=COLUMNS)


def clean_units(df: pd.DataFrame) -> pd.DataFrame:
    # Convert all columns to numeric
    for col in COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ISD-Lite scaling (tenths)
    df["temp"] /= 10.0
    df["dewpoint"] /= 10.0
    df["wind_speed"] /= 10.0
    df["sea_level_pressure"] /= 10.0

    return df


def main():
    files = sorted(RAW_DIR.glob("*.txt"))

    print("Looking for ISD-Lite files in:", RAW_DIR)
    print(f"Found {len(files)} .txt files")

    if len(files) == 0:
        raise FileNotFoundError("No ISD-Lite .txt files found")

    all_dfs = []

    for path in files:
        station = path.stem  # e.g. 724050-13743-2018
        print("Processing:", station)

        df = parse_isd_lite_file(path)
        if df.empty:
            print(f"  ⚠️ No valid rows in {path.name}")
            continue

        df = clean_units(df)

        df["station"] = station
        df["date"] = pd.to_datetime(
            dict(year=df.year, month=df.month, day=df.day),
            errors="coerce"
        )

        df = df.drop(columns=["year", "month", "day"])
        df = df[df["date"].notna()]

        all_dfs.append(df)

    if not all_dfs:
        raise ValueError("No valid meteorology data parsed from ISD-Lite files")

    met = pd.concat(all_dfs, ignore_index=True)

    out_path = OUT_DIR / "meteorology_daily_isd.csv"
    met.to_csv(out_path, index=False)

    print(f"\nSaved meteorology dataset to {out_path}")
    print("Rows:", len(met))
    print("Stations:", met["station"].unique())


if __name__ == "__main__":
    main()
