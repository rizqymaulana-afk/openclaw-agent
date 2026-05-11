# test_google_sheet.py

from google_sheets_loader import (
    GoogleSheetsLoader
)

loader = GoogleSheetsLoader()

# =========================
# SHOPEE
# =========================

shopee_df = loader.load_sheet(
    "https://docs.google.com/spreadsheets/d/1kfjTO_a1h_yH7FGRQhIZsncPx23ZZ0JW-_eLHqjHotA/edit?gid=0#gid=0",
    "SHOPEE_RAW"
)

print(
    "\n=== SHOPEE ==="
)

print(
    shopee_df.head()
)

# =========================
# TIKTOK
# =========================

tiktok_df = loader.load_sheet(
    "https://docs.google.com/spreadsheets/d/1kfjTO_a1h_yH7FGRQhIZsncPx23ZZ0JW-_eLHqjHotA/edit?gid=0#gid=0",
    "TIKTOK_RAW"
)

print(
    "\n=== TIKTOK ==="
)

print(
    tiktok_df.head()
)