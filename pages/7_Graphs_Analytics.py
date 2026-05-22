# pages/6_Graphs_Analytics.py

import streamlit as st
import plotly.express as px

st.title("📊 Analytics Dashboard")

if "data" not in st.session_state:

    st.warning("Train model first")

else:

    data = st.session_state["data"]

    prod_col = st.session_state["prod_col"]
    qty_col = st.session_state["qty_col"]
    date_col = st.session_state["date_col"]

    # PRODUCT SELECT
    product = st.selectbox(
        "Select Product",
        data[prod_col].unique()
    )

    product_data = data[
        data[prod_col] == product
    ]

    # SALES TREND
    st.subheader("📈 Daily Demand Trend")

    fig1 = px.line(
        product_data,
        x=date_col,
        y=qty_col,
        markers=True
    )

    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    