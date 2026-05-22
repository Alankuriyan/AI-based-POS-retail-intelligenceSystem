# pages/7_Fast_Slow_Products.py

import streamlit as st
import plotly.express as px

from utils import classify_product

st.title("Fast / Slow Moving Products")

if "data" not in st.session_state:

    st.warning("Train model first")

else:

    data = st.session_state["data"]

    prod_col = st.session_state["prod_col"]
    qty_col = st.session_state["qty_col"]

    speed_df = (
        data.groupby(prod_col)[qty_col]
        .mean()
        .reset_index()
    )

    speed_df["Category"] = (
        speed_df[qty_col]
        .apply(classify_product)
    )

    st.dataframe(speed_df)

    # VISUALIZATION

    fig = px.bar(
        speed_df,
        x=prod_col,
        y=qty_col,
        color="Category",
        title="Product Movement Analysis"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )