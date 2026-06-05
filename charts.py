"""
charts.py
---------
All visualization functions for the CO2 Weekly Trends dashboard.
Each function accepts a filtered DataFrame and returns a Matplotlib figure.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd

# ── Global style ────────────────────────────────────────────────────────────
PALETTE = "YlOrRd"
COLOR_MAIN = "#C0392B"
COLOR_SEC = "#E67E22"
COLOR_ACC = "#2C3E50"
BG = "#FAFAFA"
GRID_COLOR = "#DDDDDD"


def _style_ax(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=13, fontweight="bold", color=COLOR_ACC, pad=10)
    ax.set_xlabel(xlabel, fontsize=10, color=COLOR_ACC)
    ax.set_ylabel(ylabel, fontsize=10, color=COLOR_ACC)
    ax.tick_params(colors=COLOR_ACC, labelsize=9)
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)
    ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.7)


# ── 1. Pie Chart ─────────────────────────────────────────────────────────────
def chart_pie(df: pd.DataFrame) -> plt.Figure:
    """Proportional distribution of CO2 readings by Season."""
    season_avg = df.groupby("season")["co2_ppm"].mean()
    colors = ["#E74C3C", "#E67E22", "#27AE60", "#2980B9"]
    fig, ax = plt.subplots(figsize=(6, 5), facecolor=BG)
    wedges, texts, autotexts = ax.pie(
        season_avg, labels=season_avg.index, autopct="%1.1f%%",
        colors=colors, startangle=140, pctdistance=0.82,
        wedgeprops=dict(edgecolor="white", linewidth=1.5)
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title("Average CO₂ Distribution by Season", fontsize=13,
                 fontweight="bold", color=COLOR_ACC, pad=12)
    ax.legend(wedges, season_avg.index, loc="lower right", fontsize=9)
    fig.tight_layout()
    return fig


# ── 2. Histogram ─────────────────────────────────────────────────────────────
def chart_histogram(df: pd.DataFrame) -> plt.Figure:
    """Frequency distribution of weekly CO₂ readings."""
    fig, ax = plt.subplots(figsize=(7, 4), facecolor=BG)
    ax.set_facecolor(BG)
    sns.histplot(df["co2_ppm"].dropna(), bins=40, color=COLOR_MAIN,
                 edgecolor="white", ax=ax, kde=True)
    _style_ax(ax, "Histogram of Weekly CO₂ Readings", "CO₂ (ppm)", "Frequency")
    fig.tight_layout()
    return fig


# ── 3. Line Chart ────────────────────────────────────────────────────────────
def chart_line(df: pd.DataFrame) -> plt.Figure:
    """CO₂ trend over time (annual mean)."""
    annual = df.groupby("year")["co2_ppm"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(9, 4), facecolor=BG)
    ax.set_facecolor(BG)
    ax.plot(annual["year"], annual["co2_ppm"], color=COLOR_MAIN,
            linewidth=1.8, zorder=3)
    ax.fill_between(annual["year"], annual["co2_ppm"],
                    alpha=0.12, color=COLOR_MAIN)
    _style_ax(ax, "CO₂ Annual Mean Trend Over Time", "Year", "CO₂ (ppm)")
    ax.grid(axis="x", color=GRID_COLOR, linestyle="--", linewidth=0.5)
    fig.tight_layout()
    return fig


# ── 4. Bar Chart ─────────────────────────────────────────────────────────────
def chart_bar(df: pd.DataFrame) -> plt.Figure:
    """Average CO₂ per decade."""
    decade_avg = df.groupby("decade")["co2_ppm"].mean().reset_index().sort_values("decade")
    fig, ax = plt.subplots(figsize=(8, 4), facecolor=BG)
    ax.set_facecolor(BG)
    bars = ax.bar(decade_avg["decade"], decade_avg["co2_ppm"],
                  color=sns.color_palette("YlOrRd", len(decade_avg)),
                  edgecolor="white", linewidth=0.8, zorder=3)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{bar.get_height():.1f}",
                ha="center", va="bottom", fontsize=8, color=COLOR_ACC)
    _style_ax(ax, "Average CO₂ by Decade", "Decade", "CO₂ (ppm)")
    fig.tight_layout()
    return fig


# ── 5. Scatter Plot ──────────────────────────────────────────────────────────
def chart_scatter(df: pd.DataFrame) -> plt.Figure:
    """CO₂ increase since 1800 vs current CO₂ ppm."""
    plot_df = df.dropna(subset=["co2_ppm", "increase_since_1800"])
    fig, ax = plt.subplots(figsize=(7, 4), facecolor=BG)
    ax.set_facecolor(BG)
    sc = ax.scatter(plot_df["co2_ppm"], plot_df["increase_since_1800"],
                    c=plot_df["year"], cmap="YlOrRd", s=8, alpha=0.7, zorder=3)
    cbar = fig.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("Year", fontsize=9, color=COLOR_ACC)
    cbar.ax.tick_params(labelsize=8)
    _style_ax(ax, "CO₂ Level vs. Increase Since 1800",
              "CO₂ (ppm)", "Increase Since 1800 (ppm)")
    fig.tight_layout()
    return fig


# ── 6. Box Plot ──────────────────────────────────────────────────────────────
def chart_box(df: pd.DataFrame) -> plt.Figure:
    """CO₂ spread by season (box plot)."""
    fig, ax = plt.subplots(figsize=(7, 4), facecolor=BG)
    ax.set_facecolor(BG)
    season_order = ["Spring", "Summer", "Autumn", "Winter"]
    available = [s for s in season_order if s in df["season"].unique()]
    sns.boxplot(data=df, x="season", y="co2_ppm", order=available,
                palette=["#E74C3C", "#E67E22", "#27AE60", "#2980B9"],
                width=0.5, ax=ax,
                medianprops=dict(color="white", linewidth=2))
    _style_ax(ax, "CO₂ Distribution by Season (Box Plot)", "Season", "CO₂ (ppm)")
    fig.tight_layout()
    return fig


# ── 7. Heatmap ───────────────────────────────────────────────────────────────
def chart_heatmap(df: pd.DataFrame) -> plt.Figure:
    """Correlation heatmap of numeric features."""
    numeric_cols = ["co2_ppm", "co2_1yr_ago", "co2_10yr_ago",
                    "increase_since_1800", "num_days", "decimal_year"]
    corr_df = df[[c for c in numeric_cols if c in df.columns]].dropna().corr()
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG)
    sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="YlOrRd",
                linewidths=0.5, linecolor="white",
                annot_kws={"size": 9}, ax=ax,
                cbar_kws={"shrink": 0.8})
    ax.set_title("Feature Correlation Heatmap", fontsize=13,
                 fontweight="bold", color=COLOR_ACC, pad=10)
    ax.tick_params(labelsize=9, colors=COLOR_ACC)
    fig.tight_layout()
    return fig


# ── 8. Area Chart ────────────────────────────────────────────────────────────
def chart_area(df: pd.DataFrame) -> plt.Figure:
    """Cumulative CO₂ increase since 1800 over time."""
    area_df = df.dropna(subset=["increase_since_1800"]).groupby("year")["increase_since_1800"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(9, 4), facecolor=BG)
    ax.set_facecolor(BG)
    ax.fill_between(area_df["year"], area_df["increase_since_1800"],
                    color=COLOR_SEC, alpha=0.6, zorder=2)
    ax.plot(area_df["year"], area_df["increase_since_1800"],
            color=COLOR_MAIN, linewidth=1.5, zorder=3)
    _style_ax(ax, "Cumulative CO₂ Increase Since 1800 (Area Chart)",
              "Year", "Increase (ppm)")
    fig.tight_layout()
    return fig


# ── 9. Count Plot ────────────────────────────────────────────────────────────
def chart_countplot(df: pd.DataFrame) -> plt.Figure:
    """Frequency count of readings per season."""
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=BG)
    ax.set_facecolor(BG)
    season_order = ["Spring", "Summer", "Autumn", "Winter"]
    available = [s for s in season_order if s in df["season"].unique()]
    sns.countplot(data=df, x="season", order=available,
                  palette=["#E74C3C", "#E67E22", "#27AE60", "#2980B9"], ax=ax,
                  edgecolor="white")
    for bar in ax.patches:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 2,
                int(bar.get_height()),
                ha="center", va="bottom", fontsize=9, color=COLOR_ACC)
    _style_ax(ax, "Record Count by Season (Count Plot)", "Season", "Count")
    fig.tight_layout()
    return fig


# ── 10. Violin Plot ──────────────────────────────────────────────────────────
def chart_violin(df: pd.DataFrame) -> plt.Figure:
    """CO₂ distribution and probability density by decade."""
    decades = sorted(df["decade"].dropna().unique())
    top_decades = decades[-6:] if len(decades) > 6 else decades
    plot_df = df[df["decade"].isin(top_decades)]
    fig, ax = plt.subplots(figsize=(9, 4), facecolor=BG)
    ax.set_facecolor(BG)
    sns.violinplot(data=plot_df, x="decade", y="co2_ppm",
                   order=top_decades, palette="YlOrRd",
                   inner="quartile", ax=ax, linewidth=0.8)
    _style_ax(ax, "CO₂ Density Distribution by Decade (Violin Plot)",
              "Decade", "CO₂ (ppm)")
    fig.tight_layout()
    return fig
