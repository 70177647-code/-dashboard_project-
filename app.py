"""
app.py
------
Main Streamlit dashboard for NOAA CO2 Weekly Trends (Mauna Loa).
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd

from filters import load_data, apply_filters, get_kpis
from charts import (
    chart_pie, chart_histogram, chart_line, chart_bar,
    chart_scatter, chart_box, chart_heatmap, chart_area,
    chart_countplot, chart_violin
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NOAA CO₂ Weekly Trends Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #F5F5F5; }
    [data-testid="stSidebar"] { background-color: #2C3E50; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #C0392B;
    }
    .kpi-value { font-size: 26px; font-weight: 700; color: #C0392B; }
    .kpi-label { font-size: 12px; color: #666; margin-top: 4px; }
    .section-header {
        font-size: 16px; font-weight: 600; color: #2C3E50;
        border-bottom: 2px solid #E74C3C;
        padding-bottom: 4px; margin: 20px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df_full = get_data()

# ── Sidebar filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://www.noaa.gov/sites/default/files/2022-03/noaa_digital_logo-2022.png",
             width=160)
    st.markdown("## 🔧 Filters")
    st.markdown("---")

    # 1. Date/Year Range Filter
    st.markdown("**📅 Year Range**")
    year_min, year_max = int(df_full["year"].min()), int(df_full["year"].max())
    year_range = st.slider("", year_min, year_max, (year_min, year_max), key="year_slider")

    st.markdown("---")

    # 2. Category Filter — Season
    st.markdown("**🌿 Season Filter**")
    all_seasons = sorted(df_full["season"].dropna().unique())
    seasons_sel = st.multiselect("Select Season(s)", all_seasons, default=all_seasons)

    st.markdown("---")

    # 3. Numerical Range Slider — CO2
    st.markdown("**📊 CO₂ Range (ppm)**")
    co2_min = float(df_full["co2_ppm"].min())
    co2_max = float(df_full["co2_ppm"].max())
    co2_range = st.slider("", co2_min, co2_max, (co2_min, co2_max),
                          step=0.5, key="co2_slider")

    st.markdown("---")

    # 4. Multi-Select Filter — Decade
    st.markdown("**🗓 Decade Filter**")
    all_decades = sorted(df_full["decade"].dropna().unique())
    decades_sel = st.multiselect("Select Decade(s)", all_decades, default=all_decades)

    st.markdown("---")

    # 5. Search / Text Filter
    st.markdown("**🔍 Search**")
    keyword = st.text_input("Search by year, season, decade…", "")

    st.markdown("---")

    # 6. Reset Button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

# ── Apply filters ─────────────────────────────────────────────────────────────
df = apply_filters(
    df_full,
    year_range=year_range,
    seasons=seasons_sel if seasons_sel else None,
    decades=decades_sel if decades_sel else None,
    co2_range=co2_range,
    keyword=keyword
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 10px 0 4px 0;'>
  <h1 style='color:#C0392B; margin:0;'>🌍 NOAA CO₂ Weekly Trends Dashboard</h1>
  <p style='color:#666; font-size:14px; margin:4px 0 0 0;'>
    Mauna Loa Observatory · Weekly Atmospheric CO₂ Measurements (1974 – 2026)
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
kpis = get_kpis(df)
k1, k2, k3, k4, k5, k6 = st.columns(6)

def kpi_card(col, label, value):
    col.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

kpi_card(k1, "Total Records", f"{kpis['total_records']:,}")
kpi_card(k2, "Avg CO₂ (ppm)", kpis["avg_co2"])
kpi_card(k3, "Max CO₂ (ppm)", kpis["max_co2"])
kpi_card(k4, "Min CO₂ (ppm)", kpis["min_co2"])
kpi_card(k5, "Avg ↑ Since 1800", kpis["avg_increase"])
kpi_card(k6, "Year Span", kpis["year_span"])

st.markdown("<br>", unsafe_allow_html=True)

# Guard: empty data
if df.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust your selections.")
    st.stop()

# ── Section 1: Trends ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 CO₂ Trends Over Time</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(chart_line(df))
with col2:
    st.pyplot(chart_area(df))

# ── Section 2: Distributions ──────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Distributions & Spread</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)
with col3:
    st.pyplot(chart_histogram(df))
with col4:
    st.pyplot(chart_box(df))
with col5:
    st.pyplot(chart_violin(df))

# ── Section 3: Categorical Insights ───────────────────────────────────────────
st.markdown('<div class="section-header">🗂 Categorical Insights</div>', unsafe_allow_html=True)
col6, col7, col8 = st.columns(3)
with col6:
    st.pyplot(chart_pie(df))
with col7:
    st.pyplot(chart_bar(df))
with col8:
    st.pyplot(chart_countplot(df))

# ── Section 4: Relationships ───────────────────────────────────────────────────
st.markdown('<div class="section-header">🔗 Relationships & Correlations</div>', unsafe_allow_html=True)
col9, col10 = st.columns([1, 1])
with col9:
    st.pyplot(chart_scatter(df))
with col10:
    st.pyplot(chart_heatmap(df))

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#999; font-size:12px;'>"
    "Data Source: NOAA Global Monitoring Laboratory · Mauna Loa, Hawaii"
    "</p>",
    unsafe_allow_html=True
)
