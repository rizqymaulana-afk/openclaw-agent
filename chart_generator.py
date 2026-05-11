# chart_generator.py

import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator

from matplotlib.ticker import FuncFormatter

import matplotlib.patheffects as pe

import numpy as np


# =========================
# FORMAT RUPIAH
# =========================

def rupiah_formatter(
    x,
    pos
):

    return f"Rp {x:,.0f}".replace(
        ",",
        "."
    )


# =========================
# MARKETPLACE CHART
# =========================

def generate_marketplace_chart(
    marketplace_summary
):

    marketplaces = marketplace_summary.index

    revenues = marketplace_summary.values

    # =========================
    # FIGURE
    # =========================

    fig, ax = plt.subplots(
        figsize=(14, 8)
    )

    fig.patch.set_facecolor(
        "#f5f5f5"
    )

    ax.set_facecolor(
        "#f5f5f5"
    )

    # =========================
    # COLORS
    # =========================

    colors = []

    for marketplace in marketplaces:

        if marketplace == "Shopee":

            colors.append(
                "#FF6B00"
            )

        elif marketplace == "TikTok":

            colors.append(
                "#1D4ED8"
            )

        else:

            colors.append(
                "#6B7280"
            )

    # =========================
    # BARS
    # =========================

    bars = ax.bar(
        marketplaces,
        revenues,
        color=colors,
        width=0.6,
        zorder=3
    )

    # =========================
    # SHADOW EFFECT
    # =========================

    for bar in bars:

        bar.set_path_effects([
            pe.withSimplePatchShadow(
                offset=(6, -6),
                shadow_rgbFace=(
                    0,
                    0,
                    0
                ),
                alpha=0.25
            ),
            pe.Normal()
        ])

    # =========================
    # LABEL TOP BAR
    # =========================

    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x()
            + bar.get_width() / 2,

            height
            + max(revenues) * 0.02,

            f"Rp {height:,.0f}".replace(
                ",",
                "."
            ),

            ha="center",

            fontsize=18,

            fontweight="bold",

            color="#111827"
        )

    # =========================
    # TITLE
    # =========================

    ax.set_title(
        "Revenue per Marketplace",

        fontsize=32,

        fontweight="bold",

        pad=30,

        color="#111827"
    )

    # =========================
    # AXIS LABEL
    # =========================

    ax.set_xlabel(
        "Marketplace",

        fontsize=20,

        labelpad=20
    )

    ax.set_ylabel(
        "Revenue (Rupiah)",

        fontsize=20,

        labelpad=20
    )

    # =========================
    # GRID
    # =========================

    ax.grid(
        axis="y",

        linestyle="--",

        alpha=0.3,

        zorder=0
    )

    # =========================
    # FORMAT Y AXIS
    # =========================

    ax.yaxis.set_major_formatter(
        FuncFormatter(
            rupiah_formatter
        )
    )

    # =========================
    # REMOVE BORDER
    # =========================

    ax.spines[
        "top"
    ].set_visible(False)

    ax.spines[
        "right"
    ].set_visible(False)

    # =========================
    # FONT SIZE
    # =========================

    ax.tick_params(
        axis='x',
        labelsize=20
    )

    ax.tick_params(
        axis='y',
        labelsize=16
    )

    # =========================
    # SAVE
    # =========================

    output_path = (
        "marketplace_chart.png"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "\nMarketplace chart generated!"
    )

    return output_path


# =========================
# TOP PRODUCT CHART
# =========================

def generate_top_product_chart(
    df
):

    top_products = (
        df.groupby(
            "product"
        )["revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(5)
    )

    products = top_products.index

    revenues = top_products.values

    # =========================
    # FIGURE
    # =========================

    fig, ax = plt.subplots(
        figsize=(16, 9)
    )

    fig.patch.set_facecolor(
        "#f5f5f5"
    )

    ax.set_facecolor(
        "#f5f5f5"
    )

    # =========================
    # COLORS
    # =========================

    colors = [
        "#93C5FD",
        "#60A5FA",
        "#3B82F6",
        "#2563EB",
        "#1D4ED8"
    ]

    # =========================
    # BARH
    # =========================

    bars = ax.barh(
        products,
        revenues,
        color=colors,
        height=0.65,
        zorder=3
    )

    # =========================
    # SHADOW
    # =========================

    for bar in bars:

        bar.set_path_effects([
            pe.withSimplePatchShadow(
                offset=(5, -5),
                shadow_rgbFace=(
                    0,
                    0,
                    0
                ),
                alpha=0.25
            ),
            pe.Normal()
        ])

    # =========================
    # VALUE LABEL
    # =========================

    for bar in bars:

        width = bar.get_width()

        ax.text(
            width + max(revenues) * 0.01,

            bar.get_y()
            + bar.get_height() / 2,

            f"Rp {width:,.0f}".replace(
                ",",
                "."
            ),

            va="center",

            fontsize=18,

            fontweight="bold",

            color="#111827"
        )

    # =========================
    # TITLE
    # =========================

    ax.set_title(
        "Top 5 Product Revenue",

        fontsize=34,

        fontweight="bold",

        pad=25,

        color="#111827"
    )

    # =========================
    # LABEL
    # =========================

    ax.set_xlabel(
        "Revenue (Rupiah)",

        fontsize=22,

        labelpad=20
    )

    ax.set_ylabel(
        "Product",

        fontsize=22,

        labelpad=15
    )

    # =========================
    # GRID
    # =========================

    ax.grid(
        axis="x",

        linestyle="--",

        alpha=0.25,

        zorder=0
    )

    # =========================
    # FORMAT X AXIS
    # =========================

    ax.xaxis.set_major_formatter(
        FuncFormatter(
            rupiah_formatter
        )
    )

    # =========================
    # FIX OVERLAP TICK
    # =========================

    ax.xaxis.set_major_locator(
        MaxNLocator(4)
    )

    # =========================
    # IMPORTANT FIX 🔥
    # =========================

    ax.tick_params(
        axis='x',
        labelsize=14,
        rotation=0
    )

    ax.tick_params(
        axis='y',
        labelsize=14
    )

    # =========================
    # AUTO MARGIN
    # =========================

    ax.margins(
        x=0.15
    )

    # =========================
    # REMOVE BORDER
    # =========================

    ax.spines[
        "top"
    ].set_visible(False)

    ax.spines[
        "right"
    ].set_visible(False)

    # =========================
    # SAVE
    # =========================

    output_path = (
        "top_product_chart.png"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "\nTop product chart generated!"
    )

    return output_path

# =========================
# FORECAST CHART
# =========================

def generate_forecast_chart(
    df
):

    # =========================
    # DAILY REVENUE
    # =========================

    daily_revenue = (
        df.groupby(
            df["date"].dt.date
        )["revenue"]
        .sum()
        .reset_index()
    )

    daily_revenue.columns = [
        "date",
        "revenue"
    ]

    # =========================
    # SORT DATE
    # =========================

    daily_revenue = (
        daily_revenue
        .sort_values(
            by="date"
        )
    )

    # =========================
    # MOVING AVERAGE
    # =========================

    daily_revenue[
        "moving_avg"
    ] = (
        daily_revenue[
            "revenue"
        ]
        .rolling(3)
        .mean()
    )

    # =========================
    # FORECAST NEXT 7 DAYS
    # =========================

    last_avg = (
        daily_revenue[
            "moving_avg"
        ]
        .dropna()
        .iloc[-1]
    )

    forecast_days = 7

    forecast_values = []

    current_value = last_avg

    for i in range(
        forecast_days
    ):

        # random fluctuation
        fluctuation = np.random.uniform(
            0.92,
            1.08
        )

        current_value = (
            current_value
            * fluctuation
        )

        forecast_values.append(
            current_value
        )

    # =========================
    # X AXIS
    # =========================

    historical_x = list(
        range(
            len(daily_revenue)
        )
    )

    forecast_x = list(
        range(
            len(daily_revenue),
            len(daily_revenue)
            + forecast_days
        )
    )

    # =========================
    # FIGURE
    # =========================

    fig, ax = plt.subplots(
        figsize=(16, 8)
    )

    fig.patch.set_facecolor(
        "#f5f5f5"
    )

    ax.set_facecolor(
        "#f5f5f5"
    )

    # =========================
    # HISTORICAL LINE
    # =========================

    ax.plot(
        historical_x,

        daily_revenue[
            "revenue"
        ],

        linewidth=4,

        color="#2563EB",

        marker="o",

        label="Historical Revenue"
    )

    # =========================
    # FORECAST LINE
    # =========================

    ax.plot(
        forecast_x,

        forecast_values,

        linewidth=4,

        linestyle="--",

        color="#F97316",

        marker="o",

        label="Forecast"
    )

    # =========================
    # FILL AREA
    # =========================

    ax.fill_between(
        forecast_x,
        forecast_values,

        alpha=0.15,

        color="#F97316"
    )

    # =========================
    # TITLE
    # =========================

    ax.set_title(
        "Revenue Trend Forecast",

        fontsize=30,

        fontweight="bold",

        pad=25,

        color="#111827"
    )

    # =========================
    # LABEL
    # =========================

    ax.set_xlabel(
        "Timeline",

        fontsize=20
    )

    ax.set_ylabel(
        "Revenue",

        fontsize=20
    )

    # =========================
    # GRID
    # =========================

    ax.grid(
        linestyle="--",
        alpha=0.3
    )

    # =========================
    # LEGEND
    # =========================

    ax.legend(
        fontsize=14
    )

    # =========================
    # FORMAT
    # =========================

    ax.yaxis.set_major_formatter(
        FuncFormatter(
            rupiah_formatter
        )
    )

    # =========================
    # REMOVE BORDER
    # =========================

    ax.spines[
        "top"
    ].set_visible(False)

    ax.spines[
        "right"
    ].set_visible(False)

    # =========================
    # SAVE
    # =========================

    output_path = (
        "forecast_chart.png"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "\nForecast chart generated!"
    )

    return output_path