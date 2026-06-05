"""
charts.py
---------
All 10 required chart types for the CO₂ Weekly Trends Dashboard.

Every function:
  • Accepts a filtered Pandas DataFrame
  • Returns a Matplotlib Figure
  • Has a clear title, labeled axes, and a legend where applicable
  • Uses a consistent professional dark colour scheme (YlOrRd palette)

Required charts (per project spec):
  1.  Pie Chart
  2.  Histogram
  3.  Line Chart
  4.  Bar Chart
  5.  Scatter Plot
  6.  Box Plot
  7.  Heatmap
  8.  Area Chart
  9.  Count Plot
  10. Violin Plot

Course    : Exploratory Data Analysis
Instructor: Ali Hassan Sherazi
Due       : 05-June-2026
"""

import matplotlib
matplotlib.use("Agg")          # non-interactive backend for Streamlit

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

# ─── GLOBAL COLOUR SCHEME (consistent throughout) ────────────────────────────
BG      = "#0f1923"          # page background
PANEL   = "#16232f"          # chart background
GRID    = "#1e3244"          # gridlines
TEXT    = "#e8f4f8"          # primary text
MUTED   = "#7fb3c8"          # secondary text / axis labels
ACCENT  = "#e9c46a"          # yellow highlight
TEAL    = "#2a9d8f"
CORAL   = "#e76f51"
ORANGE  = "#f4a261"
NAVY    = "#264653"

SEASON_CLR = {
    "Spring": TEAL,
    "Summer": ACCENT,
    "Autumn": ORANGE,
    "Winter": NAVY,
}
DECADE_PALETTE = [NAVY, "#2a7a6f", TEAL, ACCENT, ORANGE, CORAL]
MAIN_PALETTE   = "YlOrRd"


# ─── SHARED HELPERS ──────────────────────────────────────────────────────────

def _style(fig, axes=None):
    """Apply the consistent dark theme to every axis on a figure."""
    fig.patch.set_facecolor(BG)
    for ax in (axes or fig.get_axes()):
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=TEXT, labelsize=9)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        ax.title.set_color(TEXT)
        for sp in ax.spines.values():
            sp.set_edgecolor(GRID)
        ax.grid(color=GRID, linestyle="--", linewidth=0.5, alpha=0.6)
    return fig


def _empty(title: str) -> plt.Figure:
    """Placeholder returned when filtered data is empty."""
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.text(0.5, 0.5, "No data for current filters",
            ha="center", va="center", color=MUTED, fontsize=11)
    ax.set_title(title, color=TEXT, fontsize=12, fontweight="bold")
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 1. PIE CHART — proportional distribution of a category
# ─────────────────────────────────────────────────────────────────────────────

def pie_chart(df: pd.DataFrame) -> plt.Figure:
    """Show proportion of weekly CO₂ readings by season."""
    title = "CO₂ Readings — Proportion by Season"
    if df.empty:
        return _empty(title)

    counts = df["season"].value_counts()
    colors = [SEASON_CLR.get(s, "#888") for s in counts.index]

    fig, ax = plt.subplots(figsize=(5, 4.5))
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": BG, "linewidth": 1.8},
        pctdistance=0.78,
    )
    for t in texts:
        t.set_color(TEXT); t.set_fontsize(10)
    for at in autotexts:
        at.set_color("#fff"); at.set_fontsize(9)

    ax.set_title(title, color=TEXT, fontsize=12, fontweight="bold", pad=12)
    ax.legend(counts.index, loc="lower center", bbox_to_anchor=(0.5, -0.08),
              ncol=4, fontsize=8, facecolor=PANEL, edgecolor=GRID,
              labelcolor=TEXT)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 2. HISTOGRAM — frequency distribution of a numerical column
# ─────────────────────────────────────────────────────────────────────────────

def histogram(df: pd.DataFrame) -> plt.Figure:
    """Display frequency distribution of weekly CO₂ average (ppm)."""
    title = "Distribution of Weekly CO₂ Concentrations (ppm)"
    valid = df["average"].dropna()
    if valid.empty:
        return _empty(title)

    fig, ax = plt.subplots(figsize=(6, 4))
    n, bins, patches = ax.hist(valid, bins=35, edgecolor=BG, linewidth=0.5)

    # Gradient colouring across bins
    cm = plt.cm.get_cmap(MAIN_PALETTE)
    norm_vals = (bins[:-1] - bins.min()) / (bins.max() - bins.min() + 1e-9)
    for patch, c in zip(patches, norm_vals):
        patch.set_facecolor(cm(c))

    mean_val = valid.mean()
    ax.axvline(mean_val, color=CORAL, linewidth=1.8, linestyle="--",
               label=f"Mean: {mean_val:.1f} ppm")

    ax.set_xlabel("CO₂ Concentration (ppm)", fontsize=10)
    ax.set_ylabel("Number of Weeks", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=9)
    plt.tight_layout()
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 3. LINE CHART — show trends over time
# ─────────────────────────────────────────────────────────────────────────────

def line_chart(df: pd.DataFrame) -> plt.Figure:
    """Show weekly and annual mean CO₂ trend from 1974 to 2026."""
    title = "CO₂ Concentration Trend Over Time — Mauna Loa (1974–2026)"
    valid = df.dropna(subset=["average"]).sort_values("date")
    if valid.empty:
        return _empty(title)

    annual = valid.groupby("year")["average"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(valid["date"], valid["average"],
            color=TEAL, linewidth=0.6, alpha=0.45, label="Weekly")
    ax.plot(pd.to_datetime(annual["year"].astype(str)),
            annual["average"],
            color=ACCENT, linewidth=2.2, label="Annual Mean")

    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("CO₂ (ppm)", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=9)
    plt.tight_layout()
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 4. BAR CHART — compare values across categories
# ─────────────────────────────────────────────────────────────────────────────

def bar_chart(df: pd.DataFrame) -> plt.Figure:
    """Compare average CO₂ concentration per decade."""
    title = "Average CO₂ Concentration by Decade"
    valid = df.dropna(subset=["average"])
    if valid.empty:
        return _empty(title)

    decade_avg = (
        valid.groupby("decade")["average"]
        .mean().reset_index().sort_values("decade")
    )
    colors = plt.cm.get_cmap(MAIN_PALETTE)(
        np.linspace(0.2, 0.88, len(decade_avg))
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(decade_avg["decade"], decade_avg["average"],
                  color=colors, edgecolor=BG, linewidth=0.8, width=0.6)

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{bar.get_height():.1f}",
                ha="center", va="bottom", color=TEXT, fontsize=9)

    ax.set_xlabel("Decade", fontsize=10)
    ax.set_ylabel("Average CO₂ (ppm)", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    plt.tight_layout()
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 5. SCATTER PLOT — relationship between two numerical variables
# ─────────────────────────────────────────────────────────────────────────────

def scatter_plot(df: pd.DataFrame) -> plt.Figure:
    """Show relationship between CO₂ average and increase since 1800."""
    title = "CO₂ Average vs. Increase Since Pre-Industrial Era (1800)"
    valid = df.dropna(subset=["average", "increase_since_1800"])
    if valid.empty:
        return _empty(title)

    fig, ax = plt.subplots(figsize=(6, 4))
    sc = ax.scatter(
        valid["average"],
        valid["increase_since_1800"],
        c=valid["year"],
        cmap=MAIN_PALETTE,
        s=14, alpha=0.75, edgecolors="none",
    )
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label("Year", color=TEXT, fontsize=9)
    cbar.ax.yaxis.set_tick_params(color=TEXT)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT)
    cbar.outline.set_edgecolor(GRID)

    ax.set_xlabel("CO₂ Concentration (ppm)", fontsize=10)
    ax.set_ylabel("Increase Since 1800 (ppm)", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    plt.tight_layout()
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 6. BOX PLOT — data spread, median, and outliers
# ─────────────────────────────────────────────────────────────────────────────

def box_plot(df: pd.DataFrame) -> plt.Figure:
    """Show CO₂ spread, median, and outliers per season."""
    title = "CO₂ Distribution by Season — Spread, Median & Outliers"
    valid = df.dropna(subset=["average", "season"])
    if valid.empty:
        return _empty(title)

    order = [s for s in ["Spring", "Summer", "Autumn", "Winter"]
             if s in valid["season"].unique()]

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(
        data=valid, x="season", y="average",
        hue="season", order=order,
        palette={s: SEASON_CLR[s] for s in order},
        ax=ax, linewidth=1.2, legend=False,
        flierprops={"marker":"o","markersize":3,
                    "markerfacecolor":CORAL,"alpha":0.5},
    )
    ax.set_xlabel("Season", fontsize=10)
    ax.set_ylabel("CO₂ (ppm)", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    plt.tight_layout()
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 7. HEATMAP — visualize correlation matrix of features
# ─────────────────────────────────────────────────────────────────────────────

def heatmap(df: pd.DataFrame) -> plt.Figure:
    """Visualize correlation matrix of all numeric features."""
    title = "Feature Correlation Heatmap"
    cols = ["average", "ndays", "co2_1yr_ago", "co2_10yr_ago",
            "increase_since_1800", "year", "month"]
    avail = [c for c in cols if c in df.columns]
    valid = df[avail].dropna()
    if len(valid) < 3:
        return _empty(title)

    corr = valid.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(8, 5.5))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f",
        cmap="coolwarm", ax=ax, vmin=-1, vmax=1,
        linewidths=0.4, linecolor=BG,
        cbar_kws={"shrink": 0.8},
        annot_kws={"size": 8, "color": TEXT},
    )
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(colors=TEXT)
    cbar.outline.set_edgecolor(GRID)

    plt.tight_layout()
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 8. AREA CHART — cumulative trends over time
# ─────────────────────────────────────────────────────────────────────────────

def area_chart(df: pd.DataFrame) -> plt.Figure:
    """Show cumulative annual CO₂ rise as a filled area chart."""
    title = "Annual Mean CO₂ — Cumulative Rise Over Time (Area Chart)"
    valid = df.dropna(subset=["average"])
    if valid.empty:
        return _empty(title)

    annual = valid.groupby("year")["average"].mean().reset_index()
    baseline = annual["average"].min() - 3

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(annual["year"], annual["average"], baseline,
                    alpha=0.4, color=TEAL)
    ax.plot(annual["year"], annual["average"],
            color=TEAL, linewidth=2.2, label="Annual Mean CO₂")
    ax.axhline(400, color=CORAL, linewidth=1, linestyle=":",
               label="400 ppm threshold")

    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("CO₂ (ppm)", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=9)
    plt.tight_layout()
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 9. COUNT PLOT — frequency count of categorical variables
# ─────────────────────────────────────────────────────────────────────────────

def count_plot(df: pd.DataFrame) -> plt.Figure:
    """Show frequency count of CO₂ readings per season."""
    title = "Frequency Count of CO₂ Readings per Season"
    valid = df.dropna(subset=["season"])
    if valid.empty:
        return _empty(title)

    order = [s for s in ["Spring", "Summer", "Autumn", "Winter"]
             if s in valid["season"].unique()]

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(
        data=valid, x="season", hue="season",
        order=order,
        palette={s: SEASON_CLR[s] for s in order},
        ax=ax, legend=False, edgecolor=BG,
    )
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}",
                    (p.get_x() + p.get_width() / 2, p.get_height() + 1),
                    ha="center", va="bottom", color=TEXT, fontsize=10)

    ax.set_xlabel("Season", fontsize=10)
    ax.set_ylabel("Count of Readings", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    plt.tight_layout()
    return _style(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 10. VIOLIN PLOT — distribution and probability density
# ─────────────────────────────────────────────────────────────────────────────

def violin_plot(df: pd.DataFrame) -> plt.Figure:
    """Show CO₂ distribution and probability density per decade."""
    title = "CO₂ Distribution & Probability Density by Decade (Violin Plot)"
    valid = df.dropna(subset=["average", "decade"])
    if valid.empty or valid["decade"].nunique() < 2:
        return _empty(title)

    decades = sorted(valid["decade"].unique())
    colors  = plt.cm.get_cmap(MAIN_PALETTE)(
        np.linspace(0.15, 0.9, len(decades))
    )

    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.violinplot(
        data=valid, x="decade", y="average",
        hue="decade", order=decades,
        palette={d: c for d, c in zip(decades, colors)},
        ax=ax, legend=False, inner="quartile", linewidth=1.0,
    )
    ax.set_xlabel("Decade", fontsize=10)
    ax.set_ylabel("CO₂ (ppm)", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    plt.tight_layout()
    return _style(fig)
