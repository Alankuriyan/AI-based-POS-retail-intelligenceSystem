import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(page_title="POS System", layout="wide")

st.title("🛒 POS SYSTEM")
st.markdown("Smart Billing System (Rates from rates.csv)")

# ---------------------------------------------------
# CLEAN FUNCTION
# ---------------------------------------------------

def clean(x):
    return str(x).strip().lower()

# ---------------------------------------------------
# INVENTORY LOAD
# ---------------------------------------------------

stock_file = "inventory/stock_data.csv"

if not os.path.exists(stock_file):
    st.error("Inventory not found")
    st.stop()

stock_df = pd.read_csv(stock_file)

stock_df["Product"] = stock_df["Product"].apply(clean)
stock_df["Stock"] = pd.to_numeric(stock_df["Stock"], errors="coerce").fillna(0).astype(int)

# ---------------------------------------------------
# LOAD RATES FROM rates.csv (ONLY SOURCE)
# ---------------------------------------------------

rate_file = "rates.csv"

if not os.path.exists(rate_file):
    st.error("rates.csv not found")
    st.stop()

rate_df = pd.read_csv(rate_file)

if "Product" not in rate_df.columns or "Avg_Rate" not in rate_df.columns:
    st.error("rates.csv format must be: Product, Avg_Rate")
    st.stop()

rate_df["Product"] = rate_df["Product"].apply(clean)
rate_df["Avg_Rate"] = pd.to_numeric(rate_df["Avg_Rate"], errors="coerce").fillna(0)

price_map = dict(zip(rate_df["Product"], rate_df["Avg_Rate"]))

# ---------------------------------------------------
# CART INIT
# ---------------------------------------------------

if "cart" not in st.session_state:
    st.session_state["cart"] = {}

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

search = st.text_input("🔍 Search Product")

if search:
    stock_df = stock_df[
        stock_df["Product"].str.contains(clean(search), case=False)
    ]

# ---------------------------------------------------
# PRODUCT GRID
# ---------------------------------------------------

st.markdown("## 📦 Products")

cols = st.columns(4)

for idx, row in stock_df.iterrows():

    col = cols[idx % 4]

    product = row["Product"]
    stock = int(row["Stock"])

    # RATE ONLY FROM rates.csv
    rate = price_map.get(product, 0.0)

    with col:

        st.markdown(f"""
        <div style="
            padding:15px;
            border-radius:15px;
            border:1px solid #2d3748;
            background:#111827;
            color:white;
            text-align:center;
            margin-bottom:10px;
        ">
            <h4>{product}</h4>
            <p>Stock: {stock}</p>
            <p>Rate: ₹ {round(rate,2)}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("➕ Add", key=f"add_{product}_{idx}"):

            if product in st.session_state["cart"]:
                st.session_state["cart"][product]["Qty"] += 1
            else:
                st.session_state["cart"][product] = {
                    "Qty": 1,
                    "Rate": float(rate)
                }

            st.rerun()

# ---------------------------------------------------
# CART
# ---------------------------------------------------

st.sidebar.title("🛒 CART")

cart = st.session_state["cart"]

if not cart:
    st.sidebar.info("Cart is empty")

else:

    total = 0
    rows = []

    for product, details in cart.items():

        qty = details["Qty"]
        rate = details["Rate"]

        total_price = qty * rate
        total += total_price

        rows.append({
            "Product": product,
            "Qty": qty,
            "Rate": rate,
            "Total": total_price
        })

    df = pd.DataFrame(rows)

    st.sidebar.dataframe(df, use_container_width=True)
    st.sidebar.metric("💰 Total", f"₹ {total:.2f}")

    # ---------------------------------------------------
    # CHECKOUT
    # ---------------------------------------------------

    if st.sidebar.button("💳 Checkout"):

        bill_no = str(uuid.uuid4())[:8]
        date = datetime.now().strftime("%Y-%m-%d")

        ledger_rows = []

        for product, details in cart.items():

            ledger_rows.append({
                "Date": date,
                "Bill_No": bill_no,
                "Product": product,
                "Qty": details["Qty"],
                "Rate": details["Rate"],
                "Total": details["Qty"] * details["Rate"]
            })

        ledger_df = pd.DataFrame(ledger_rows)

        ledger_path = "ledger/sales_ledger.csv"
        os.makedirs("ledger", exist_ok=True)

        if os.path.exists(ledger_path):
            old = pd.read_csv(ledger_path)
            ledger_df = pd.concat([old, ledger_df], ignore_index=True)

        ledger_df.to_csv(ledger_path, index=False)

        # ---------------------------------------------------
        # STOCK UPDATE
        # ---------------------------------------------------

        for product, details in cart.items():

            mask = stock_df["Product"] == product

            if mask.any():
                stock_df.loc[mask, "Stock"] -= details["Qty"]

        stock_df["Stock"] = stock_df["Stock"].clip(lower=0)
        stock_df.to_csv(stock_file, index=False)

        # RESET
        st.success("Checkout successful!")
        st.session_state["cart"] = {}
        st.rerun()