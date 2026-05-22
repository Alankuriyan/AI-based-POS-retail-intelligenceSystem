import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.title(" Next Week Forecast")

# ---------------------------------------------------
# CLEAN FUNCTION (IMPORTANT FIX)
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
    # LOAD DATA
    # ---------------------------------------------------

    data = st.session_state["data"]

    prod_col = st.session_state["prod_col"]
    date_col = st.session_state["date_col"]
    price_col = st.session_state["price_col"]

    # ---------------------------------------------------
    # LOAD STOCK CSV (ONLY SOURCE)
    # ---------------------------------------------------

    stock_file = "inventory/stock_data.csv"

    if os.path.exists(stock_file) and os.path.getsize(stock_file) > 0:

        stock_df = pd.read_csv(stock_file)

        stock_df["Product"] = stock_df["Product"].astype(str).apply(clean)
        stock_df["Stock"] = pd.to_numeric(stock_df["Stock"], errors="coerce").fillna(0)

    else:
        st.error("stock_data.csv not found")
        st.stop()

    # ---------------------------------------------------
    # PRODUCT SELECT
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

    predictions = []

    lag = p["lag_1"]

    # ---------------------------------------------------
    # FORECAST BUTTON
    # ---------------------------------------------------

    if st.button("Forecast Next 7 Days"):

        for i in range(7):

            row = [[
                p["prod_id"],
                p[price_col],
                np.log1p(p[price_col]),
                p["price_ratio"],
                p["month"],
                p["day"],
                p["week"],
                p["day_of_week"],
                p["is_weekend"],
                lag,
                p["lag_7"],
                p["trend_3"],
                p["trend_7"]
            ]]

            pred_log = st.session_state["model"].predict(row)[0]
            pred = int(np.expm1(pred_log))

            predictions.append(pred)

            lag = pred

        # ---------------------------------------------------
        # TABLE
        # ---------------------------------------------------

        forecast_df = pd.DataFrame({
            "Day": [
                "Day 1","Day 2","Day 3",
                "Day 4","Day 5","Day 6","Day 7"
            ],
            "Predicted Demand": predictions
        })

        st.dataframe(forecast_df, use_container_width=True)

        # ---------------------------------------------------
        # CHART
        # ---------------------------------------------------

        fig = px.line(
            forecast_df,
            x="Day",
            y="Predicted Demand",
            markers=True,
            title="📈 Next Week Demand Forecast"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------------------
        # STOCK FETCH (FIXED)
        # ---------------------------------------------------

        stock_match = stock_df[
            stock_df["Product"] == product_clean
        ]

        if stock_match.empty:
            current_stock = 0
            st.warning("⚠ Product not found in stock_data.csv")
        else:
            current_stock = int(stock_match.iloc[0]["Stock"])

        # ---------------------------------------------------
        # ANALYSIS
        # ---------------------------------------------------

        weekly_demand = sum(predictions)

        remaining_stock = current_stock - weekly_demand

        usage_percent = 0
        if current_stock > 0:
            usage_percent = (weekly_demand / current_stock) * 100

        # ---------------------------------------------------
        # STATUS
        # ---------------------------------------------------

        if remaining_stock <= 0:
            status = "🔴 Weekly Stock Risk"
        elif remaining_stock <= 5:
            status = "🟠 Critical Weekly Stock"
        elif remaining_stock <= 15:
            status = "🟡 Low Weekly Stock"
        else:
            status = "🟢 Weekly Stock Healthy"

        # ---------------------------------------------------
        # OUTPUT
        # ---------------------------------------------------

        st.subheader("📦 Weekly Inventory Analysis")

        c1, c2, c3 = st.columns(3)

        c1.metric("📦 Current Stock", current_stock)
        c2.metric("📈 Weekly Demand", weekly_demand)
        c3.metric("📉 Remaining Stock", remaining_stock)

        st.info(status)

        st.metric("📊 Stock Usage %", f"{usage_percent:.2f}%")

        # ---------------------------------------------------
        # RESTOCK SUGGESTION
        # ---------------------------------------------------

        if remaining_stock <= 15:

            suggested = abs(remaining_stock) + 50

            st.error(f"""
⚠ Product may run out this week

Suggested Restock: {suggested} units
""")