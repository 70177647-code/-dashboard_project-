"""
filters.py
----------
Data loading, cleaning, preprocessing, and filter logic.

Dataset : co2_weekly_mlo.csv  (DO NOT rename — per project spec)
Course  : Exploratory Data Analysis
Instructor: Ali Hassan Sherazi
Due     : 05-June-2026
"""

import pandas as pd
import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# 1.  LOAD & CLEAN
# ─────────────────────────────────────────────────────────────────────────────

def load_data(filepath: str = "data/co2_weekly_mlo.csv") -> pd.DataFrame:
    """
    Load the NOAA Mauna Loa weekly CO₂ dataset and perform all cleaning /
    feature-engineering steps required for the dashboard.

    Cleaning steps
    --------------
    1. Skip comment lines (lines starting with '#') using comment='#'
    2. Replace NOAA missing-value sentinel -999.99 with NaN
    3. Build a proper datetime column from year / month / day
    4. Engineer 'season'  (Spring / Summer / Autumn / Winter)
    5. Engineer 'decade'  ('1970s', '1980s', …)
    6. Rename verbose column names to short, usable aliases
    """

    # ── Step 1: read CSV, skip comment lines ──────────────────────────────────
    df = pd.read_csv(filepath, comment="#")

    # ── Step 2: replace missing-value sentinel with NaN ───────────────────────
    df.replace(-999.99, np.nan, inplace=True)

    # ── Step 3: build proper datetime column ──────────────────────────────────
    df["date"] = pd.to_datetime(
        df[["year", "month", "day"]].astype(int), errors="coerce"
    )

    # ── Step 4: season (categorical) — Spring / Summer / Autumn / Winter ──────
    season_map = {
        12: "Winter",  1: "Winter",  2: "Winter",
         3: "Spring",  4: "Spring",  5: "Spring",
         6: "Summer",  7: "Summer",  8: "Summer",
         9: "Autumn", 10: "Autumn", 11: "Autumn",
    }
    df["season"] = df["month"].map(season_map)

    # ── Step 5: decade (categorical) — used for bar chart & violin plot ────────
    df["decade"] = (df["year"] // 10 * 10).astype(str) + "s"

    # ── Step 6: rename verbose column names ───────────────────────────────────
    df.rename(columns={
        "1 year ago":          "co2_1yr_ago",
        "10 years ago":        "co2_10yr_ago",
        "increase since 1800": "increase_since_1800",
    }, inplace=True)

    return df


# ─────────────────────────────────────────────────────────────────────────────
# 2.  FILTER
# ─────────────────────────────────────────────────────────────────────────────

def apply_filters(
    df: pd.DataFrame,
    year_range: tuple,
    selected_seasons: list,
    co2_range: tuple,
    selected_decade: str,
    search_year: str,
) -> pd.DataFrame:
    """
    Apply all six sidebar filter controls to the dataframe.
    Returns a filtered *copy* — never mutates the original.

    Filters
    -------
    1. Date / Time Range  — year slider
    2. Numerical Range    — CO₂ concentration (ppm) slider
    3. Multi-Select       — season checkboxes
    4. Category Dropdown  — decade selector
    5. Text / Search      — free-text year search
    (Reset handled in app.py via st.rerun())
    """
    filtered = df.copy()

    # 1. Year range
    filtered = filtered[
        (filtered["year"] >= year_range[0]) &
        (filtered["year"] <= year_range[1])
    ]

    # 2. CO₂ numerical range
    filtered = filtered[
        (filtered["average"] >= co2_range[0]) &
        (filtered["average"] <= co2_range[1])
    ]

    # 3. Season multi-select
    if selected_seasons:
        filtered = filtered[filtered["season"].isin(selected_seasons)]

    # 4. Decade dropdown
    if selected_decade != "All":
        filtered = filtered[filtered["decade"] == selected_decade]

    # 5. Text / year search
    if search_year.strip():
        filtered = filtered[
            filtered["year"].astype(str).str.contains(search_year.strip())
        ]

    return filtered


# ─────────────────────────────────────────────────────────────────────────────
# 3.  KPI HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_kpis(df: pd.DataFrame) -> dict:
    """Compute KPI summary values for the top metric cards."""
    valid = df["average"].dropna()
    inc   = df["increase_since_1800"].dropna()
    return {
        "total_records": len(df),
        "avg_co2":       round(float(valid.mean()),  2) if len(valid) else 0,
        "max_co2":       round(float(valid.max()),   2) if len(valid) else 0,
        "min_co2":       round(float(valid.min()),   2) if len(valid) else 0,
        "latest_co2":    round(float(valid.iloc[-1]),2) if len(valid) else 0,
        "total_increase":round(float(inc.iloc[-1]),  2) if len(inc)   else 0,
    }
