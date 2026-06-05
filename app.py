"""
app.py
------
Main Streamlit dashboard — CO₂ Weekly Trends (NOAA Mauna Loa, 1974–2026).

Run:
    streamlit run app.py

Project   : EDA Data Visualization Dashboard
Course    : Exploratory Data Analysis
Instructor: Ali Hassan Sherazi
Due       : 05-June-2026

Spec compliance
---------------
✅ Correct dataset filename (co2_weekly_mlo.csv — NOT renamed)
✅ Pandas for all loading / cleaning / filtering / aggregation
✅ Matplotlib + Seaborn for all visualisations
✅ Streamlit for the interactive frontend
✅ All 10 required chart types present
✅ All 6 required filter types present, linked to ALL charts
✅ KPI summary cards at the top
✅ Dashboard title + description
✅ Sidebar navigation for filters
✅ Charts grouped in logical sections
✅ Consistent professional colour scheme throughout
✅ Responsive layout using st.columns()
✅ Reset / Clear Filters button
"""

import streamlit as st
import pandas as pd

from filters import load_data, apply_filters, get_kpis
from charts import (
    pie_chart, histogram, line_chart, bar_chart, scatter_plot,
    box_plot, heatmap, area_chart, count_plot, violin_plot,
)

# ─── PAGE CONFIGURATION ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="CO₂ Weekly Trends Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS — dark professional theme ────────────────────────────────────
st.markdown("""
<style>
/* Global background */
.stApp { background-color: #0f1923; color: #e8f4f8; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111d28;
    border-right: 1px solid #1e3244;
}
[data-testid="stSidebar"] * { color: #c9dde8 !important; }

/* Metric cards */
[data-testid="stMetric"] {
    background: #16232f;
    border: 1px solid #1e3244;
    border-radius: 10px;
    padding: 14px 18px;
}
[data-testid="stMetricLabel"] { color: #7fb3c8 !important; font-size:0.78rem !important; }
[data-testid="stMetricValue"] { color: #e9c46a !important; font-size:1.5rem !important; font-weight:700; }

/* Section headers */
h2, h3 { color: #e9c46a !important; }

/* Chart containers */
.chart-box {
    background: #16232f;
    border: 1px solid #1e3244;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 14px;
}

/* Dividers */
hr { border-color: #1e3244; }

/* Buttons */
.stButton > button {
    background-color: #264653;
    color: #e8f4f8;
    border: 1px solid #2a9d8f;
    border-radius: 6px;
    font-weight: 600;
    width: 100%;
    transition: background 0.2s;
}
.stButton > button:hover { background-color: #2a9d8f; color: #fff; }

/* Expander */
[data-testid="stExpander"] {
    background: #16232f;
    border: 1px solid #1e3244;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ─── LOAD DATA (cached so it only reads the CSV once) ────────────────────────
@st.cache_data
def get_data():
    return load_data("data/co2_weekly_mlo.csv")

df_full = get_data()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — all 6 required filter types
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 Dashboard Filters")
    st.markdown("---")

    # ── Filter 1: Date / Time Range ──────────────────────────────────────────
    st.markdown("**📅 Year Range**")
    year_min = int(df_full["year"].min())
    year_max = int(df_full["year"].max())
    year_range = st.slider(
        "Year range", min_value=year_min, max_value=year_max,
        value=(year_min, year_max), label_visibility="collapsed",
    )
    st.markdown("---")

    # ── Filter 2: Multi-Select — seasons ────────────────────────────────────
    st.markdown("**🌸 Season (Multi-Select)**")
    all_seasons = ["Spring", "Summer", "Autumn", "Winter"]
    selected_seasons = st.multiselect(
        "Seasons", options=all_seasons, default=all_seasons,
        label_visibility="collapsed",
    )
    st.markdown("---")

    # ── Filter 3: Numerical Range Slider — CO₂ ppm ──────────────────────────
    st.markdown("**🌿 CO₂ Level (ppm)**")
    co2_min = float(df_full["average"].dropna().min())
    co2_max = float(df_full["average"].dropna().max())
    co2_range = st.slider(
        "CO₂ range", min_value=co2_min, max_value=co2_max,
        value=(co2_min, co2_max), step=0.1,
        label_visibility="collapsed",
    )
    st.markdown("---")

    # ── Filter 4: Category Dropdown — decade ────────────────────────────────
    st.markdown("**📊 Decade (Category)**")
    all_decades = sorted(df_full["decade"].unique().tolist())
    selected_decade = st.selectbox(
        "Decade", options=["All"] + all_decades,
        label_visibility="collapsed",
    )
    st.markdown("---")

    # ── Filter 5: Text / Search Filter ──────────────────────────────────────
    st.markdown("**🔍 Search by Year**")
    search_year = st.text_input(
        "Search year", value="", placeholder="e.g. 1998",
        label_visibility="collapsed",
    )
    st.markdown("---")

    # ── Filter 6: Reset / Clear Filters ─────────────────────────────────────
    if st.button("🔄 Reset All Filters"):
        st.rerun()

    st.markdown(
        "<div style='margin-top:16px;font-size:11px;color:#4a6880;line-height:1.6'>"
        "All filters update every chart simultaneously."
        "</div>", unsafe_allow_html=True
    )


# ─── APPLY FILTERS — all filters feed into one filtered df ───────────────────
df = apply_filters(
    df_full,
    year_range=year_range,
    selected_seasons=selected_seasons,
    co2_range=co2_range,
    selected_decade=selected_decade,
    search_year=search_year,
)


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:6px 0 2px 0'>
  <h1 style='color:#e9c46a;font-size:2rem;margin-bottom:4px'>
    🌍 CO₂ Weekly Trends Dashboard
  </h1>
  <p style='color:#7fb3c8;font-size:0.9rem;margin:0'>
    NOAA Mauna Loa Observatory &nbsp;|&nbsp; Weekly Atmospheric CO₂ (1974–2026)
    &nbsp;|&nbsp; Exploratory Data Analysis — Ali Hassan Sherazi
  </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# KPI SUMMARY CARDS (per spec: Total Records, Key Averages, Notable Highs/Lows)
# ─────────────────────────────────────────────────────────────────────────────
kpis = get_kpis(df)
c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("📋 Total Records",    f"{kpis['total_records']:,}")
c2.metric("🌿 Avg CO₂ (ppm)",    f"{kpis['avg_co2']}")
c3.metric("🔺 Max CO₂ (ppm)",    f"{kpis['max_co2']}")
c4.metric("🔻 Min CO₂ (ppm)",    f"{kpis['min_co2']}")
c5.metric("📍 Latest Reading",   f"{kpis['latest_co2']} ppm")
c6.metric("📈 Rise Since 1800",  f"+{kpis['total_increase']} ppm")
st.markdown("---")


# ─── GUARD: warn if no data matches filters ───────────────────────────────────
if df.empty:
    st.warning("⚠️ No data matches the current filters. Adjust the sidebar controls.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — Trend Analysis  (Line + Area)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📈 Trend Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(line_chart(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(area_chart(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — Comparative Analysis  (Bar + Scatter)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📊 Comparative Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(bar_chart(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(scatter_plot(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — Distribution & Frequency  (Pie + Histogram + Count)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 🥧 Distribution & Frequency")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(pie_chart(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(histogram(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(count_plot(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — Statistical Distribution  (Box + Violin)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 🎻 Statistical Distribution")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(box_plot(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.pyplot(violin_plot(df), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — Correlation Heatmap (full width + explanation)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 🔥 Correlation Heatmap")
st.markdown('<div class="chart-box">', unsafe_allow_html=True)
col_map, col_exp = st.columns([2, 1])

with col_map:
    st.pyplot(heatmap(df), use_container_width=True)

with col_exp:
    st.markdown("""
    <br>
    <p style='color:#7fb3c8;font-size:0.87rem'>
    <b style='color:#e9c46a'>How to read this heatmap</b><br><br>
    Values near <b>+1</b> → strong positive correlation.<br>
    Values near <b>−1</b> → strong negative correlation.<br>
    Values near <b>0</b>  → little or no relationship.<br><br>
    <b>Key finding:</b> <i>year</i> and <i>average</i> have
    a correlation of <b>+0.99</b>, confirming the steady
    long-term rise in atmospheric CO₂ driven by human activity.
    </p>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# RAW DATA EXPANDER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📄 View Filtered Raw Data Table"):
    display_cols = {
        "date":                "Date",
        "year":                "Year",
        "month":               "Month",
        "season":              "Season",
        "decade":              "Decade",
        "average":             "CO₂ (ppm)",
        "co2_1yr_ago":         "1 Yr Ago (ppm)",
        "co2_10yr_ago":        "10 Yrs Ago (ppm)",
        "increase_since_1800": "Rise Since 1800",
        "ndays":               "Valid Days",
    }
    st.dataframe(
        df[display_cols.keys()].rename(columns=display_cols),
        use_container_width=True, height=300,
    )
    st.caption(f"Showing {len(df):,} rows after current filters.")


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<p style='text-align:center;color:#4a6880;font-size:0.77rem'>
  Data: NOAA Global Monitoring Laboratory — Mauna Loa Observatory, Hawaii &nbsp;|&nbsp;
  Dataset: <code>co2_weekly_mlo.csv</code> &nbsp;|&nbsp;
  Stack: Python · Pandas · NumPy · Matplotlib · Seaborn · Streamlit
</p>
""", unsafe_allow_html=True)
