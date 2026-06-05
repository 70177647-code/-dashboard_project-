# 🌍 CO₂ Weekly Trends Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Submission:** 05-June-2026 | Portal Submission  
**Dataset:** `co2_weekly_mlo.csv` — NOAA Mauna Loa Weekly CO₂ (1974–2026)

---

## Project Overview

An interactive data visualization dashboard that explores 52 years of weekly
atmospheric CO₂ measurements from the Mauna Loa Observatory, Hawaii.  
Built with **Python, Pandas, Matplotlib, Seaborn, and Streamlit**.

---

## Folder Structure

```
dashboard_project/
├── data/
│   └── co2_weekly_mlo.csv        ← EXACT original filename (DO NOT rename)
├── notebooks/
│   └── analysis.ipynb            ← EDA notebook
├── app.py                        ← Main Streamlit dashboard
├── charts.py                     ← All 10 chart functions
├── filters.py                    ← Data loading, cleaning & filter logic
├── requirements.txt              ← Python dependencies
└── README.md
```

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch dashboard
streamlit run app.py
```

Opens at **http://localhost:8501** in your browser automatically.

---

## All 10 Required Charts

| # | Chart | What it shows |
|---|-------|--------------|
| 1 | Pie Chart | Proportion of readings per season |
| 2 | Histogram | Frequency distribution of weekly CO₂ (ppm) |
| 3 | Line Chart | CO₂ trend week-by-week from 1974 to 2026 |
| 4 | Bar Chart | Average CO₂ concentration per decade |
| 5 | Scatter Plot | CO₂ average vs. increase since 1800 |
| 6 | Box Plot | CO₂ spread, median & outliers per season |
| 7 | Heatmap | Correlation matrix of all numeric features |
| 8 | Area Chart | Cumulative CO₂ rise shown as filled area |
| 9 | Count Plot | Number of readings recorded per season |
| 10 | Violin Plot | Full CO₂ distribution + density per decade |

---

## All 6 Required Filters (all linked to all charts)

| Filter | Type | Description |
|--------|------|-------------|
| Year Range | Slider | Filter by year (1974–2026) |
| Season | Multi-select | Spring / Summer / Autumn / Winter |
| CO₂ Level | Range slider | Filter by ppm concentration |
| Decade | Dropdown | Focus on a single decade |
| Search Year | Text input | Type any year to isolate it |
| Reset | Button | Clears all filters to defaults |

---

## Data Cleaning Steps (Pandas)

1. `comment='#'` — skips NOAA comment lines at top of CSV
2. `.replace(-999.99, np.nan)` — replaces missing-value sentinel with NaN
3. `pd.to_datetime(...)` — builds proper datetime column from year/month/day
4. `season_map` — engineers Spring/Summer/Autumn/Winter from month number
5. `decade` — engineers "1980s", "1990s" etc. for grouped analysis
6. `.rename(columns={...})` — shortens verbose NOAA column names

---

## Key Insights

- CO₂ rose from **~330 ppm (1974)** to **~432 ppm (2026)** — +102 ppm in 52 years
- Clear **seasonal cycle** every year: spring peak, autumn dip (plant activity)
- Rate of increase has **accelerated**: ~1 ppm/yr (1970s) → ~2.5 ppm/yr (2020s)
- `year` and `average` have **r = 0.99** correlation — near-perfect linear trend
- CO₂ crossed the **400 ppm milestone** in 2013 for the first time in human history
- 20 weeks have **missing readings** (coded as -999.99 in raw data), all handled

---

## Technical Stack

| Tool | Role |
|------|------|
| Python 3.x | Core language |
| Pandas | Data loading, cleaning, filtering, aggregation |
| NumPy | Numerical operations |
| Matplotlib | Core chart creation |
| Seaborn | Statistical visualizations & styling |
| Streamlit | Interactive frontend dashboard |
