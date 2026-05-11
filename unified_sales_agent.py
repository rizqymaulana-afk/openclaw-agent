# unified_sales_agent.py

from urllib import response

import pandas as pd
try:

    import ollama

    OLLAMA_AVAILABLE = True

except:

    OLLAMA_AVAILABLE = False
from datetime import datetime

from google_sheets_loader import (
    GoogleSheetsLoader
)

from telegram_sender import (
    send_message,
    send_photo
)

from chart_generator import (
    generate_marketplace_chart,
    generate_top_product_chart,
    generate_forecast_chart
)

from memory_manager import (
    MemoryManager
)


class UnifiedSalesAgent:

    def __init__(self):

        self.all_data = []

        self.loader = GoogleSheetsLoader()

        self.memory_manager = MemoryManager()

    # =========================
    # FORMAT RUPIAH
    # =========================

    def format_rupiah(
        self,
        value
    ):

        return f"Rp {value:,.0f}".replace(
            ",",
            "."
        )

    # =========================
    # CLEAN CURRENCY
    # =========================

    def clean_currency(
        self,
        value
    ):

        if pd.isna(value):

            return 0

        # =========================
        # FLOAT CASE
        # =========================

        if isinstance(
            value,
            float
        ):

            return int(
                value * 1000
            )

        # =========================
        # STRING CASE
        # =========================

        value = str(value)

        value = (
            value
            .replace("Rp", "")
            .replace(" ", "")
            .replace(".", "")
            .replace(",", "")
            .replace("\n", "")
            .strip()
        )

        try:

            return int(value)

        except:

            return 0

    # =========================
    # NORMALIZE DATA
    # =========================

    def normalize_data(
        self,
        df,
        mapping,
        marketplace
    ):

        normalized = pd.DataFrame()

        # =========================
        # DATE
        # =========================

        normalized["date"] = pd.to_datetime(
            df[
                mapping["date"]
            ],
            dayfirst=True,
            errors="coerce"
        )

        # =========================
        # PRODUCT
        # =========================

        normalized["product"] = df[
            mapping["product"]
        ]

        # =========================
        # QTY
        # =========================

        normalized["qty"] = pd.to_numeric(
            df[
                mapping["qty"]
            ],
            errors="coerce"
        )

        # =========================
        # DEBUG RAW REVENUE
        # =========================

        print(
            "\n=== RAW REVENUE SAMPLE ==="
        )

        print(
            df[
                mapping["revenue"]
            ].head(10)
        )

        # =========================
        # CLEAN REVENUE
        # =========================

        normalized["revenue"] = df[
            mapping["revenue"]
        ].apply(
            self.clean_currency
        )

        # =========================
        # DEBUG CLEAN REVENUE
        # =========================

        print(
            "\n=== CLEAN REVENUE SAMPLE ==="
        )

        print(
            normalized[
                "revenue"
            ].head(10)
        )

        # =========================
        # MARKETPLACE
        # =========================

        normalized[
            "marketplace"
        ] = marketplace

        return normalized

    # =========================
    # LOAD GOOGLE SHEET
    # =========================

    def load_google_sheet(
        self,
        spreadsheet_url,
        worksheet_name,
        mapping,
        marketplace
    ):

        print(
            f"\nLoading {marketplace}..."
        )

        df = self.loader.load_sheet(
            spreadsheet_url,
            worksheet_name
        )

        normalized = self.normalize_data(
            df,
            mapping,
            marketplace
        )

        self.all_data.append(
            normalized
        )

        print(
            f"{marketplace} loaded!"
        )

    # =========================
    # MERGE DATA
    # =========================

    def merge_data(
        self
    ):

        print(
            "\nMerging all marketplace..."
        )

        merged = pd.concat(
            self.all_data,
            ignore_index=True
        )

        return merged

    # =========================
    # FILTER LATEST DATA
    # =========================

    def filter_today_data(
        self,
        df
    ):

        print(
            "\nFiltering latest transaction date..."
        )

        # =========================
        # EMPTY DATA
        # =========================

        if df.empty:

            print(
                "Dataset kosong!"
            )

            return df

        # =========================
        # GET LATEST DATE
        # =========================

        latest_date = (
            df[
                "date"
            ]
            .dropna()
            .dt.date
            .max()
        )

        print(
            f"Latest Date: {latest_date}"
        )

        # =========================
        # FILTER
        # =========================

        filtered = df[
            df[
                "date"
            ].dt.date == latest_date
        ]

        print(
            f"Filtered Transactions: {len(filtered)}"
        )

        # =========================
        # DEBUG DATE SAMPLE
        # =========================

        print(
            "\n=== DATE SAMPLE ==="
        )

        print(
            filtered[
                "date"
            ].head()
        )

        return filtered

    # =========================
    # ANALYZE
    # =========================

    def analyze(
        self,
        df
    ):

        print(
            "\n=== SALES ANALYSIS ==="
        )

        # =========================
        # EMPTY DATA PROTECTION
        # =========================

        if df.empty:

            print(
                "No transactions found!"
            )

            return {

                "total_revenue": "Rp 0",

                "total_revenue_numeric": 0,

                "total_orders": 0,

                "top_marketplace": "-",

                "top_product": "-",

                "marketplace_summary": pd.Series(
                    dtype=float
                )
            }

        total_revenue = df[
            "revenue"
        ].sum()

        total_orders = len(df)

        top_marketplace = df.groupby(
            "marketplace"
        )[
            "revenue"
        ].sum().idxmax()

        top_product = df.groupby(
            "product"
        )[
            "revenue"
        ].sum().idxmax()

        marketplace_summary = df.groupby(
            "marketplace"
        )[
            "revenue"
        ].sum()

        # =========================
        # DEBUG MARKETPLACE
        # =========================

        print(
            "\n=== MARKETPLACE SUMMARY ==="
        )

        for marketplace, revenue in marketplace_summary.items():

            print(
                f"{marketplace}: "
                f"{self.format_rupiah(revenue)}"
            )

        print(
            f"\nTotal Revenue : "
            f"{self.format_rupiah(total_revenue)}"
        )

        print(
            f"Total Orders : "
            f"{total_orders}"
        )

        print(
            f"Top Marketplace : "
            f"{top_marketplace}"
        )

        print(
            f"Top Product : "
            f"{top_product}"
        )

        return {

            "total_revenue": self.format_rupiah(
                total_revenue
            ),

            "total_revenue_numeric": int(
                total_revenue
            ),

            "total_orders": total_orders,

            "top_marketplace": top_marketplace,

            "top_product": top_product,

            "marketplace_summary": marketplace_summary
        }

    # =========================
    # GROWTH ANALYSIS
    # =========================

    def analyze_growth(
        self,
        analysis
    ):

        previous_data = (
            self.memory_manager.load_memory()
        )

        if not previous_data:

            return (
                "Belum ada data pembanding "
                "hari sebelumnya."
            )

        current_revenue = analysis[
            "total_revenue_numeric"
        ]

        previous_revenue = previous_data[
            "total_revenue"
        ]

        if previous_revenue == 0:

            return (
                "Belum ada revenue "
                "hari sebelumnya."
            )

        growth = (
            (
                current_revenue
                - previous_revenue
            )
            / previous_revenue
        ) * 100

        if growth > 0:

            return (
                f"Revenue meningkat "
                f"{growth:.1f}% "
                f"dibanding hari sebelumnya."
            )

        elif growth < 0:

            return (
                f"Revenue menurun "
                f"{abs(growth):.1f}% "
                f"dibanding hari sebelumnya."
            )

        return (
            "Revenue stabil dibanding "
            "hari sebelumnya."
        )

    # =========================
    # FORECAST ANALYSIS
    # =========================

    def forecast_monthly_revenue(
        self,
        analysis
    ):

        current_revenue = analysis[
            "total_revenue_numeric"
        ]

        days_in_month = 31

        projected_revenue = (
            current_revenue
            * days_in_month
        )

        forecast_text = (
            f"Jika performa harian stabil, "
            f"proyeksi revenue bulanan "
            f"dapat mencapai "
            f"{self.format_rupiah(projected_revenue)}."
        )

        return forecast_text

        # =========================
    # AI INSIGHT
    # =========================

    def generate_ai_insight(
        self,
        analysis,
        growth_analysis,
        forecast_analysis,
        selected_date
    ):

        print(
            "\nGenerating AI insight..."
        )

        today_date = selected_date.strftime(
            "%d %B %Y"
        )

        marketplace_summary = analysis[
            "marketplace_summary"
        ]

        total_revenue_numeric = max(
            1,
            sum(
                marketplace_summary.values
            )
        )

        marketplace_lines = ""

        for marketplace, revenue in marketplace_summary.items():

            percentage = (
                revenue
                / total_revenue_numeric
            ) * 100

            marketplace_lines += (
                f"- {marketplace}: "
                f"{self.format_rupiah(revenue)} "
                f"({percentage:.1f}%)\n"
            )

        prompt = f"""
Kamu adalah Senior Business Analyst
untuk brand parfum Scentplus Indonesia.

WAJIB FULL BAHASA INDONESIA.

DATA:

Tanggal:
{today_date}

Total Revenue:
{analysis['total_revenue']}

Total Orders:
{analysis['total_orders']}

Top Marketplace:
{analysis['top_marketplace']}

Top Product:
{analysis['top_product']}

Marketplace Performance:
{marketplace_lines}

Growth Analysis:
{growth_analysis}

Forecast Analysis:
{forecast_analysis}

FORMAT:

📊 Daily Report - {today_date}

📌 Ringkasan Bisnis

📈 Insight Penting

✅ Kesimpulan
"""

        if not OLLAMA_AVAILABLE:

            return f"""
        📊 Daily Report - {today_date}

        📌 Ringkasan Bisnis

        Total revenue hari ini sebesar
        {analysis['total_revenue']}
        dengan total order
        {analysis['total_orders']} transaksi.

        Marketplace teratas:
        {analysis['top_marketplace']}

        Produk terlaris:
        {analysis['top_product']}

        📈 Insight Penting

        {growth_analysis}

        🔮 Forecast

        {forecast_analysis}

        ✅ Kesimpulan

        Performa penjualan menunjukkan
        tren yang positif dan stabil.
        """

        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response[
            "message"
        ]["content"]

# =========================
# MAIN
# =========================

agent = UnifiedSalesAgent()

SPREADSHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1kfjTO_a1h_yH7FGRQhIZsncPx23ZZ0JW-_eLHqjHotA/edit?gid=0#gid=0"
)

# =========================
# SHOPEE
# =========================

shopee_mapping = {

    "date": "Waktu Pesanan Dibuat",

    "product": "Nama Produk",

    "qty": "Jumlah",

    "revenue": "Harga Setelah Diskon"
}

agent.load_google_sheet(
    SPREADSHEET_URL,
    "SHOPEE_RAW",
    shopee_mapping,
    "Shopee"
)

# =========================
# TIKTOK
# =========================

tiktok_mapping = {

    "date": "Created Time",

    "product": "Product Name",

    "qty": "Quantity",

    "revenue": "SKU Subtotal After Discount"
}

agent.load_google_sheet(
    SPREADSHEET_URL,
    "TIKTOK_RAW",
    tiktok_mapping,
    "TikTok"
)

# =========================
# MERGE
# =========================

merged_data = agent.merge_data()

# =========================
# FILTER LATEST
# =========================

today_data = agent.filter_today_data(
    merged_data
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

print(
    "\n=== GROWTH ANALYSIS ==="
)

print(
    growth_analysis
)

# =========================
# FORECAST ANALYSIS
# =========================

forecast_analysis = (
    agent.forecast_monthly_revenue(
        analysis
    )
)

print(
    "\n=== FORECAST ANALYSIS ==="
)

print(
    forecast_analysis
)

# =========================
# AI INSIGHT
# =========================

ai_summary = (
    agent.generate_ai_insight(
        analysis,
        growth_analysis,
        forecast_analysis,
        datetime.now()
    )
)

print(
    "\n=== AI INSIGHT ===\n"
)

print(
    ai_summary
)

# =========================
# CHART
# =========================

chart_path = generate_marketplace_chart(
    analysis[
        "marketplace_summary"
    ]
)

top_product_chart = (
    generate_top_product_chart(
        today_data
    )
)

forecast_chart = (
    generate_forecast_chart(
        merged_data
    )
)

print(
    "\nChart generated!"
)

# =========================
# TELEGRAM
# =========================

telegram_report = ai_summary

print(
    "\nSending Telegram report..."
)

send_message(
    telegram_report
)

send_photo(
    chart_path,
    "📈 Revenue per Marketplace"
)

send_photo(
    top_product_chart,
    "🏆 Top 5 Product Revenue"
)

send_photo(
    forecast_chart,
    "🔮 Revenue Trend Forecast"
)

# =========================
# SAVE MEMORY
# =========================

agent.memory_manager.save_memory({

    "date": str(
        datetime.now().date()
    ),

    "total_revenue": analysis[
        "total_revenue_numeric"
    ],

    "marketplace_summary": {

        key: int(value)

        for key, value in analysis[
            "marketplace_summary"
        ].items()
    }
})

print(
    "\nTelegram report sent!"
)