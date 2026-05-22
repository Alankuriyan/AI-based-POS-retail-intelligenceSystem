import streamlit as st
import numpy as np
import pandas as pd
import os

st.title(" Next Day Prediction")

# ---------------------------------------------------
# CLEAN FUNCTION (IMPORTANT)
# ---------------------------------------------------

def clean(x):
    return str(x).strip().lower()

# ---------------------------------------------------
# CHECK MODEL
# ---------------------------------------------------

if "model" not in st.session_state:
    st.warning("Train model first")

else:

    # ---------------------------------------------------
    # LOAD DATASET (FOR MODEL FEATURES)
    # ---------------------------------------------------

    data = st.session_state["data"]

    prod_col = st.session_state["prod_col"]
    price_col = st.session_state["price_col"]
    date_col = st.session_state["date_col"]

    # ---------------------------------------------------
    # LOAD STOCK FROM CSV (ONLY SOURCE OF TRUTH)
    # ---------------------------------------------------

    stock_file = "inventory/stock_data.csv"

    if os.path.exists(stock_file) and os.path.getsize(stock_file) > 0:

        stock_df = pd.read_csv(stock_file)

        # CLEAN STOCK DATA
        stock_df["Product"] = stock_df["Product"].astype(str).apply(clean)
        stock_df["Stock"] = pd.to_numeric(stock_df["Stock"], errors="coerce").fillna(0)

    else:
        st.error("stock_data.csv not found")
        st.stop()

    # ---------------------------------------------------
    # PRODUCT SELECTION
    # ---------------------------------------------------

    product = st.selectbox(
        "Select Product",
        data[prod_col].unique()
    )

    product_clean = clean(product)

    product_data = data[
        data[prod_col] == product
    ].sort_values(by=date_col)

    p = product_data.iloc[-1]

    # ---------------------------------------------------
    # PRICE INPUT
    # ---------------------------------------------------

    price = st.number_input(
        "Product Price",
        value=float(p[price_col])
    )

    # ---------------------------------------------------
    # PREDICTION
    # ---------------------------------------------------

    if st.button("Predict Demand"):

        row = [[
            p["prod_id"],
            price,
            np.log1p(price),
            p["price_ratio"],
            p["month"],
            p["day"],
            p["week"],
            p["day_of_week"],
            p["is_weekend"],
            p["lag_1"],
            p["lag_7"],
            p["trend_3"],
            p["trend_7"]
        ]]

        pred_log = st.session_state["model"].predict(row)[0]
        pred = int(np.expm1(pred_log))

        # ---------------------------------------------------
        # FETCH STOCK (STRICT MATCH FROM CSV)
        # ---------------------------------------------------

        match = stock_df[
            stock_df["Product"] == product_clean
        ]

        if match.empty:
            current_stock = 0
            st.warning("⚠ Product not found in stock_data.csv")
        else:
            current_stock = int(match.iloc[0]["Stock"])

        # ---------------------------------------------------
        # ANALYSIS
        # ---------------------------------------------------

        remaining_stock = current_stock - pred

        usage_percent = 0
        if current_stock > 0:
            usage_percent = (pred / current_stock) * 100

        # ---------------------------------------------------
        # STATUS
        # ---------------------------------------------------

        if remaining_stock <= 0:
            status = "🔴 Out of Stock Risk"
        elif remaining_stock <= 5:
            status = "🟠 Critical Stock"
        elif remaining_stock <= 15:
            status = "🟡 Low Stock"
        else:
            status = "🟢 Healthy"

        # ---------------------------------------------------
        # OUTPUT
        # ---------------------------------------------------

        st.subheader("📊 Prediction Analysis")

        c1, c2, c3 = st.columns(3)

        c1.metric("📦 Current Stock", current_stock)
        c2.metric("📈 Predicted Demand", pred)
        c3.metric("📉 Remaining Stock", remaining_stock)

        st.info(status)

        st.metric("📊 Stock Usage %", f"{usage_percent:.2f}%")

        # ---------------------------------------------------
        # RESTOCK SUGGESTION
        # ---------------------------------------------------

        if remaining_stock <= 5:

            suggested = abs(remaining_stock) + 20

            st.error(f"""
⚠ Product may run out soon

Suggested Restock: {suggested} units
""")

        # ---------------------------------------------------
        # TREND ANALYSIS
        # ---------------------------------------------------

        if p["trend_7"] > p["trend_3"]:
            st.success("📈 Short-Term Trend Increasing")
        else:
            st.warning("📉 Short-Term Trend Decreasing")