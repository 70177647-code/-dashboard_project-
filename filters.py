"""
filters.py
----------
Data loading, cleaning, and filtering functions for the CO2 Weekly Trends dashboard.
"""

import pandas as pd
import numpy as np


def load_data(filepath: str = None) -> pd.DataFrame:
    """Load and clean the NOAA CO2 weekly dataset."""
    # Skip comment lines starting with '#'
    url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_weekly_mlo.csv"
    df = pd.read_csv(url, comment="#")
    df.columns = df.columns.str.strip()

    # Replace sentinel value -999.99 with NaN
    df.replace(-999.99, np.nan, inplace=True)

    # Create a proper datetime column
    df["date"] = pd.to_datetime(
        df[["year", "month", "day"]].rename(columns={"year": "year", "month": "month", "day": "day"}),
        errors="coerce"
    )

    # Rename columns for clarity
    df.rename(columns={
        "average": "co2_ppm",
        "1 year ago": "co2_1yr_ago",
        "10 years ago": "co2_10yr_ago",
        "increase since 1800": "increase_since_1800",
        "decimal": "decimal_year",
        "ndays": "num_days"
    }, inplace=True)

    # Drop rows with no CO2 reading
    df = df.dropna(subset=["co2_ppm"])

    # Decade column for grouping
    df["decade"] = (df["year"] // 10 * 10).astype(str) + "s"

    # Season column
    df["season"] = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })

    return df.sort_values("date").reset_index(drop=True)


def apply_filters(
    df: pd.DataFrame,
    year_range: tuple = None,
    seasons: list = None,
    decades: list = None,
    co2_range: tuple = None,
    keyword: str = ""
) -> pd.DataFrame:
    """Apply all sidebar filters and return the filtered DataFrame."""
    filtered = df.copy()

    # Year range filter
    if year_range:
        filtered = filtered[(filtered["year"] >= year_range[0]) & (filtered["year"] <= year_range[1])]

    # Season multi-select filter
    if seasons:
        filtered = filtered[filtered["season"].isin(seasons)]

    # Decade filter
    if decades:
        filtered = filtered[filtered["decade"].isin(decades)]

    # Numerical CO2 range slider
    if co2_range:
        filtered = filtered[(filtered["co2_ppm"] >= co2_range[0]) & (filtered["co2_ppm"] <= co2_range[1])]

    # Keyword / text search filter (matches year, month, season, decade as string)
    if keyword.strip():
        kw = keyword.strip().lower()
        mask = (
            filtered["year"].astype(str).str.contains(kw) |
            filtered["season"].str.lower().str.contains(kw) |
            filtered["decade"].str.lower().str.contains(kw) |
            filtered["month"].astype(str).str.contains(kw)
        )
        filtered = filtered[mask]

    return filtered.reset_index(drop=True)


def get_kpis(df: pd.DataFrame) -> dict:
    """Return a dictionary of KPI summary values."""
    return {
        "total_records": len(df),
        "avg_co2": round(df["co2_ppm"].mean(), 2),
        "max_co2": round(df["co2_ppm"].max(), 2),
        "min_co2": round(df["co2_ppm"].min(), 2),
        "avg_increase": round(df["increase_since_1800"].mean(), 2),
        "year_span": f"{int(df['year'].min())} – {int(df['year'].max())}"
    }
