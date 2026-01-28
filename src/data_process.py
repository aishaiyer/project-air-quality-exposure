"""
PM2.5 Data Processing Script

- Reads EPA AQS daily PM2.5 (FRM/FEM, 88101) files
- Filters to DC and Maryland
- Performs basic quality control
- Outputs a single tidy dataset for analysis
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_pm25_files():
    files = sorted(RAW_DIR.glob("daily_88101_*.csv"))
    if not files:
        raise FileNotFoundError("No PM2.5 daily files found in data/raw/")
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = f.name
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def filter_region(df):
    return df[df["State Name"].isin(["District Of Columbia", "Maryland"])]


def select_columns(df):
    keep = [
        "State Name",
        "County Name",
        "Site Num",
        "Latitude",
        "Longitude",
        "Date Local",
        "Arithmetic Mean",
        "Units of Measure",
        "Sample Duration",
        "Observation Count",
        "source_file",
    ]
    return df[keep]


def basic_qc(df):
    df = df[df["Arithmetic Mean"].notna()]
    return df


def main():
    # 1) Load
    df = load_pm25_files()
    print("Loaded:", len(df))
    print("Columns:", list(df.columns)[:30])

    # 2) Region filter
    df = filter_region(df)
    print("After region filter:", len(df))
    if len(df) == 0:
        print("Unique State Name values (sample):", df["State Name"].dropna().unique()[:10])

    # 3) Column selection
    df = select_columns(df)
    print("After select columns:", len(df))

    # 4) QC
    # Print units BEFORE filtering so we can see what the file actually uses
    print("Units (unique, sample):", df["Units of Measure"].dropna().unique()[:10])
    print("Sample Duration (unique, sample):", df["Sample Duration"].dropna().unique()[:10])

    df = basic_qc(df)
    print("After QC:", len(df))

    # 5) Parse date and save
    df["date"] = pd.to_datetime(df["Date Local"], errors="coerce")
    df = df.drop(columns=["Date Local"])
    df = df[df["date"].notna()]  # drop any rows with bad dates

    out_path = OUT_DIR / "pm25_daily_dc_md.csv"
    df.to_csv(out_path, index=False)

    print(f"Saved cleaned dataset to {out_path}")
    print(f"Rows saved: {len(df):,}")



if __name__ == "__main__":
    main()
