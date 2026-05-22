
import streamlit as st
import pandas as pd
import os

st.title("📂 Upload Dataset")

file = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if file:

    # ---------------------------------------------------
    # CREATE DATASET FOLDER
    # ---------------------------------------------------

    os.makedirs(
        "datasets",
        exist_ok=True
    )

    # ---------------------------------------------------
    # SAVE FILE
    # ---------------------------------------------------

    save_path = os.path.join(
        "datasets",
        file.name
    )

    with open(save_path, "wb") as f:

        f.write(file.getbuffer())

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------

    df = (
        pd.read_csv(save_path)
        if file.name.endswith("csv")
        else pd.read_excel(save_path)
    )

    st.session_state["raw_df"] = df

    st.success(
        "✅ Dataset Uploaded & Saved"
    )

    st.write(
        f"Saved to: {save_path}"
    )

    st.dataframe(df.head())