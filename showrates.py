
import joblib
import pandas as pd

# ---------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------

DATA_PATH = "models/processed_data.pkl"

data = joblib.load(DATA_PATH)

print("\n📦 LOADED DATASET\n")
print("Columns:", data.columns.tolist())

# ---------------------------------------------------
# COLUMN CONFIG
# ---------------------------------------------------

prod_col = "Product Name"
price_col = "Rate"

# ---------------------------------------------------
# SAFETY CHECK
# ---------------------------------------------------

if prod_col not in data.columns or price_col not in data.columns:
    raise Exception(f"Missing columns: {prod_col} or {price_col}")

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------

df = data[[prod_col, price_col]].copy()

df[prod_col] = df[prod_col].astype(str).str.strip().str.lower()
df[price_col] = pd.to_numeric(df[price_col], errors="coerce")

df = df.dropna()

# ---------------------------------------------------
# CREATE PRICE MAP
# ---------------------------------------------------

price_map = (
    df.groupby(prod_col)[price_col]
    .mean()
    .reset_index()
)

price_map.columns = ["Product", "Avg_Rate"]
price_map = price_map.sort_values("Product")

# ---------------------------------------------------
# SHOW
# ---------------------------------------------------

print("\n📊 PRODUCT RATES\n")
print(price_map.to_string(index=False))

# ---------------------------------------------------
# SAVE FILES
# ---------------------------------------------------

price_map.to_csv("product_rates.csv", index=False)
price_map.to_csv("rates.csv", index=False)

print("\n✅ Saved: product_rates.csv + rates.csv\n")