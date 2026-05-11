# dashboard.py

import streamlit as st

from unified_sales_agent import (
    UnifiedSalesAgent
)

from chart_generator import (
    generate_marketplace_chart,
    generate_top_product_chart,
    generate_forecast_chart
)

from streamlit_autorefresh import (
    st_autorefresh
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(

    page_title="AI Sales Dashboard",

    layout="wide"
)

# =========================
# AUTO REFRESH
# =========================

st_autorefresh(

    interval=600000,

    key="dashboard_refresh"
)

# =========================
# TITLE
# =========================

st.title(
    "🚀 AI Sales Dashboard"
)

st.markdown(
    "### Live Business Intelligence System"
)

# =========================
# INIT AGENT
# =========================

agent = UnifiedSalesAgent()

SPREADSHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1kfjTO_a1h_yH7FGRQhIZsncPx23ZZ0JW-_eLHqjHotA/edit?gid=0#gid=0"
)

# =========================
# LOAD DATA
# =========================

shopee_mapping = {

    "date": "Waktu Pesanan Dibuat",

    "product": "Nama Produk",

    "qty": "Jumlah",

    "revenue": "Harga Setelah Diskon"
}

tiktok_mapping = {

    "date": "Created Time",

    "product": "Product Name",

    "qty": "Quantity",

    "revenue": "SKU Subtotal After Discount"
}

# =========================
# LOADING
# =========================

with st.spinner(
    "Loading marketplace data..."
):

    # =========================
    # SHOPEE
    # =========================

    agent.load_google_sheet(
        SPREADSHEET_URL,
        "SHOPEE_RAW",
        shopee_mapping,
        "Shopee"
    )

    # =========================
    # TIKTOK
    # =========================

    agent.load_google_sheet(
        SPREADSHEET_URL,
        "TIKTOK_RAW",
        tiktok_mapping,
        "TikTok"
    )

# =========================
# MERGE DATA
# =========================

merged_data = agent.merge_data()

# =========================
# SIDEBAR
# =========================

st.sidebar.title(
    "📌 Filter Dashboard"
)

# =========================
# MARKETPLACE FILTER
# =========================

marketplace_options = (
    merged_data[
        "marketplace"
    ]
    .unique()
    .tolist()
)

selected_marketplace = (
    st.sidebar.multiselect(

        "Pilih Marketplace",

        marketplace_options,

        default=marketplace_options
    )
)

# =========================
# DATE FILTER
# =========================

min_date = (
    merged_data[
        "date"
    ]
    .min()
    .date()
)

max_date = (
    merged_data[
        "date"
    ]
    .max()
    .date()
)

selected_date = (
    st.sidebar.date_input(

        "Pilih Tanggal",

        value=max_date,

        min_value=min_date,

        max_value=max_date
    )
)

# =========================
# FILTER DATA
# =========================

filtered_data = merged_data[

    (
        merged_data[
            "marketplace"
        ].isin(
            selected_marketplace
        )
    )

    &

    (
        merged_data[
            "date"
        ].dt.date
        == selected_date
    )
]

# =========================
# FILTER LATEST DATA
# =========================

today_data = agent.filter_today_data(
    filtered_data
)

# =========================
# ANALYSIS
# =========================

analysis = agent.analyze(
    today_data
)

# =========================
# GROWTH ANALYSIS
# =========================

growth_analysis = (
    agent.analyze_growth(
        analysis
    )
)

# =========================
# FORECAST ANALYSIS
# =========================

forecast_analysis = (
    agent.forecast_monthly_revenue(
        analysis
    )
)

# =========================
# AI INSIGHT
# =========================

ai_summary = (
    agent.generate_ai_insight(
        analysis,
        growth_analysis,
        forecast_analysis,
        selected_date
    )
)

# =========================
# KPI SECTION
# =========================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "💰 Total Revenue",

        analysis[
            "total_revenue"
        ]
    )

with col2:

    st.metric(

        "🛒 Total Orders",

        analysis[
            "total_orders"
        ]
    )

with col3:

    st.metric(

        "🏆 Top Marketplace",

        analysis[
            "top_marketplace"
        ]
    )

# =========================
# MARKETPLACE CHART
# =========================

st.markdown("---")

st.subheader(
    "📈 Revenue per Marketplace"
)

marketplace_chart = (
    generate_marketplace_chart(
        analysis[
            "marketplace_summary"
        ]
    )
)

st.image(
    marketplace_chart
)

# =========================
# TOP PRODUCT CHART
# =========================

st.markdown("---")

st.subheader(
    "🏆 Top Product Revenue"
)

top_product_chart = (
    generate_top_product_chart(
        today_data
    )
)

st.image(
    top_product_chart
)

# =========================
# FORECAST CHART
# =========================

st.markdown("---")

st.subheader(
    "🔮 Revenue Forecast"
)

forecast_chart = (
    generate_forecast_chart(
        merged_data
    )
)

st.image(
    forecast_chart
)

# =========================
# AI INSIGHT
# =========================

st.markdown("---")

st.subheader(
    "🤖 AI Business Insight"
)

st.markdown(
    ai_summary
)

# =========================
# GROWTH ANALYSIS
# =========================

st.markdown("---")

st.subheader(
    "📊 Growth Analysis"
)

st.success(
    growth_analysis
)

# =========================
# FORECAST ANALYSIS
# =========================

st.markdown("---")

st.subheader(
    "🚀 Forecast Projection"
)

st.info(
    forecast_analysis
)

# =========================
# RAW DATA
# =========================

st.markdown("---")

st.subheader(
    "🧾 Raw Transaction Data"
)

st.dataframe(
    today_data,
    use_container_width=True
)

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption(
    "AI Sales Dashboard • Powered by OpenClaw Agent"
)