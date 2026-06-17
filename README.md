# 🌍 NOAA CO₂ Weekly Trends Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Dataset:** `co2_weekly_mlo.csv` — NOAA Weekly CO₂ Readings, Mauna Loa Observatory (1974–2026)  
**Submission Date:** 05-June-2026

---

## 📌 Project Overview

This dashboard visualizes over 50 years of atmospheric CO₂ measurements from Mauna Loa, Hawaii. It provides interactive filtering, 10 professional chart types, and KPI summary cards — all built with Python, Pandas, Matplotlib, Seaborn, and Streamlit.

---

## ⚙️ Installation

1. **Clone / unzip** the project folder.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```
4. Open your browser at `http://localhost:8501`

> ⚠️ Make sure the file `data/co2_weekly_mlo.csv` is present. Do **not** rename it.

---

## 📁 Folder Structure

```
dashboard_project/
├── data/
│   └── co2_weekly_mlo.csv          ← Original dataset (do not rename)
├── notebooks/
│   └── analysis.ipynb              ← EDA notebook
├── app.py                          ← Main Streamlit dashboard
├── charts.py                       ← All 10 chart functions
├── filters.py                      ← Data loading, cleaning, filter logic
├── requirements.txt                ← Python dependencies
└── README.md                       ← This file
```

---

## 🗂 Dataset Description

| Column | Description |
|--------|-------------|
| `year`, `month`, `day` | Date of reading |
| `decimal` | Decimal year (e.g., 1974.38) |
| `average` | Weekly mean CO₂ in ppm |
| `ndays` | Number of days contributing to reading |
| `1 year ago` | CO₂ reading from 365 days ago |
| `10 years ago` | CO₂ reading from ~10 years ago |
| `increase since 1800` | Estimated rise from pre-industrial baseline |

Sentinel value `-999.99` = missing data (replaced with NaN during cleaning).

---

## 📊 Charts Included

| # | Chart Type | Insight |
|---|-----------|---------|
| 1 | Pie Chart | CO₂ share by season |
| 2 | Histogram | Frequency of CO₂ readings |
| 3 | Line Chart | Annual CO₂ trend over time |
| 4 | Bar Chart | Average CO₂ per decade |
| 5 | Scatter Plot | CO₂ vs increase since 1800 |
| 6 | Box Plot | CO₂ spread per season |
| 7 | Heatmap | Feature correlation matrix |
| 8 | Area Chart | Cumulative CO₂ rise since 1800 |
| 9 | Count Plot | Record count per season |
| 10 | Violin Plot | CO₂ density distribution by decade |

---

## 🔧 Filters

All filters are in the sidebar and dynamically update **all charts simultaneously**:

- 📅 Year Range Slider
- 🌿 Season Multi-Select
- 📊 CO₂ Range Slider
- 🗓 Decade Multi-Select
- 🔍 Keyword Search
- 🔄 Reset All Filters Button

---

## 🔍 Key Insights

1. **Steady rise:** CO₂ has risen from ~333 ppm in 1974 to over 430 ppm in 2026 — an increase of nearly 100 ppm in 50 years.
2. **Seasonal cycle:** CO₂ peaks in spring (May) and dips in autumn (September/October) due to Northern Hemisphere plant activity.
3. **Accelerating growth:** Decade-over-decade comparisons show the rate of CO₂ increase has itself been increasing.
4. **Strong correlation:** CO₂ ppm and increase-since-1800 are near-perfectly correlated (r ≈ 1.0), confirming the anthropogenic baseline.
5. **Missing data pattern:** Early years (1970s) have more `-999.99` sentinel values, reflecting less complete measurement infrastructure.
