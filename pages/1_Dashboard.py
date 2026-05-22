# pages/1_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

from components.metric_cards import metric_card

st.set_page_config(
    page_title="AI Retail Dashboard",
    layout="wide"
)

st.title("AI Retail Forecast Dashboard")

# ---------------------------------------------------
# CHECK DATA
# ---------------------------------------------------

if "data" not in st.session_state:

    st.warning("Upload dataset and train model first")

else:

    data = st.session_state["data"].copy()

    prod_col = st.session_state["prod_col"]
    qty_col = st.session_state["qty_col"]
    price_col = st.session_state["price_col"]
    date_col = st.session_state["date_col"]

    # ---------------------------------------------------
    # DATE FORMAT
    # ---------------------------------------------------

    data[date_col] = pd.to_datetime(data[date_col])

    # ---------------------------------------------------
    # REVENUE FIELDS
    # ---------------------------------------------------

    if "Taxable Amount" not in data.columns:
        data["Taxable Amount"] = data[qty_col] * data[price_col]

    if "GST Amount" not in data.columns:
        data["GST Amount"] = 0

    if "Net Amount" not in data.columns:
        data["Net Amount"] = data["Taxable Amount"] + data["GST Amount"]

    # ---------------------------------------------------
    # MONTH FILTER
    # ---------------------------------------------------

    data["Month"] = data[date_col].dt.to_period("M").astype(str)

    months = sorted(data["Month"].unique())

    selected_months = st.multiselect(
        "Select Months",
        months,
        default=months
    )

    filtered_data = data[data["Month"].isin(selected_months)]

    # ---------------------------------------------------
    # KPIs
    # ---------------------------------------------------

    total_products = filtered_data[prod_col].nunique()
    total_units = int(filtered_data[qty_col].sum())
    net_revenue = int(filtered_data["Net Amount"].sum())

    total_days = filtered_data[date_col].nunique()
    total_days = max(total_days, 1)

    daily_revenue = int(net_revenue / total_days)

    avg_transaction = int(net_revenue / max(len(filtered_data), 1))

    top_product = filtered_data.groupby(prod_col)[qty_col].sum().idxmax()

    fast_products = (filtered_data.groupby(prod_col)[qty_col].mean() >= 50).sum()
    slow_products = (filtered_data.groupby(prod_col)[qty_col].mean() < 20).sum()

    # ---------------------------------------------------
    # KPI ROW 1
    # ---------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Products", total_products, "")

    with col2:
        metric_card("Units Sold", f"{total_units:,}", "")

    with col3:
        metric_card("Daily Revenue", f"₹ {daily_revenue:,}", "")

    # ---------------------------------------------------
    # KPI ROW 2
    # ---------------------------------------------------

    col4, col5, col6 = st.columns(3)

    with col4:
        metric_card("Avg Transaction", f"₹ {avg_transaction:,}", "")

    with col5:
        metric_card("Fast Moving", fast_products, "")

    with col6:
        metric_card("Slow Moving", slow_products, "")

    # ---------------------------------------------------
    # AI INSIGHTS
    # ---------------------------------------------------

    st.markdown(f"""
    <div class="glass-card">

    <h2>AI Retail Insights</h2>

    <ul>

    <li>Top Product: <b>{top_product}</b></li>

    <li>Selected Months Revenue: <b>₹ {net_revenue:,}</b></li>

    <li>Average Daily Revenue: <b>₹ {daily_revenue:,}</b></li>

    <li>Average Transaction: <b>₹ {avg_transaction:,}</b></li>

    <li>Fast Moving Products: <b>{fast_products}</b></li>

    <li>Slow Moving Products: <b>{slow_products}</b></li>

    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ---------------------------------------------------
    # SALES TREND
    # ---------------------------------------------------

    st.subheader("Daily Sales Trend")

    sales_df = filtered_data.groupby(date_col)[qty_col].sum().reset_index()

    fig1 = px.line(
        sales_df,
        x=date_col,
        y=qty_col,
        markers=True,
        title="Daily Product Sales"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ---------------------------------------------------
    # REVENUE TREND
    # ---------------------------------------------------

    st.subheader("Revenue Trend")

    revenue_df = filtered_data.groupby(date_col)["Net Amount"].sum().reset_index()

    fig2 = px.area(
        revenue_df,
        x=date_col,
        y="Net Amount",
        title="Revenue Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------------------------
    # TOP PRODUCTS
    # ---------------------------------------------------

    st.subheader("Top Products")

    top_df = (
        filtered_data.groupby(prod_col)[qty_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(
        top_df,
        x=prod_col,
        y=qty_col,
        title="Top Selling Products"
    )

    st.plotly_chart(fig4, use_container_width=True)