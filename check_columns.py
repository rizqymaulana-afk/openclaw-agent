import pandas as pd

# =========================
# SHOPEE
# =========================

print("\n=== SHOPEE COLUMNS ===\n")

shopee_df = pd.read_csv(
    "data/shopee/DB_Pesanan - SHOPEE_RAW.csv"
)

for col in shopee_df.columns:

    print(col)

# =========================
# TIKTOK
# =========================

print("\n=== TIKTOK COLUMNS ===\n")

tiktok_df = pd.read_csv(
    "data/tiktok/DB_Pesanan - TIKTOK_RAW.csv"
)

for col in tiktok_df.columns:

    print(col)