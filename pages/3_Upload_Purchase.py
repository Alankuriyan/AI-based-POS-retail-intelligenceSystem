

import streamlit as st
import pandas as pd
import os

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------

st.title("📥 Upload Purchase Data")

st.markdown("""
Upload cleaned purchase CSV extracted from PDF.
The system will clean broken rows automatically
and update inventory stock.
""")

# ---------------------------------------------------
# CREATE FOLDERS
# ---------------------------------------------------

os.makedirs("datasets", exist_ok=True)
os.makedirs("ledger", exist_ok=True)
os.makedirs("inventory", exist_ok=True)

# ---------------------------------------------------
# FILE PATHS
# ---------------------------------------------------

purchase_dataset_path = "datasets/purchase.csv"

ledger_path = "ledger/purchase_ledger.csv"

stock_file = "inventory/stock_data.csv"

# ---------------------------------------------------
# FILE UPLOADER
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Purchase CSV",
    type=["csv"]
)

# ---------------------------------------------------
# PROCESS FILE
# ---------------------------------------------------

if uploaded_file is not None:

    try:

        # -------------------------------------------
        # READ CSV
        # -------------------------------------------

        df = pd.read_csv(
            uploaded_file
        )

        # -------------------------------------------
        # CLEAN COLUMN NAMES
        # -------------------------------------------

        df.columns = (
            df.columns
            .str.strip()
        )

        # -------------------------------------------
        # REMOVE UNWANTED COLUMN
        # -------------------------------------------

        df = df.drop(
            columns=["N"],
            errors="ignore"
        )

        # -------------------------------------------
        # AUTO DETECT PRODUCT COLUMN
        # -------------------------------------------

        possible_product_cols = [

            "Product_Name",
            "Product",
            "product",
            "Item"
        ]

        product_col = None

        for col in possible_product_cols:

            if col in df.columns:

                product_col = col
                break

        # -------------------------------------------
        # CHECK PRODUCT COLUMN
        # -------------------------------------------

        if product_col is None:

            st.error(
                "❌ Product column not found"
            )

            st.stop()

        # -------------------------------------------
        # CHECK QTY COLUMN
        # -------------------------------------------

        if "Qty" not in df.columns:

            st.error(
                "❌ Qty column not found"
            )

            st.stop()

        # -------------------------------------------
        # CLEAN PRODUCT NAMES
        # -------------------------------------------

        df[product_col] = (

            df[product_col]
            .astype(str)

            .str.replace('"', '')

            .str.replace(",", " ")

            .str.replace("  ", " ")

            .str.strip()
        )

        # -------------------------------------------
        # CLEAN QTY
        # -------------------------------------------

        df["Qty"] = pd.to_numeric(
            df["Qty"],
            errors="coerce"
        )

        # -------------------------------------------
        # REMOVE BAD ROWS
        # -------------------------------------------

        df = df.dropna(
            subset=["Qty"]
        )

        df = df[
            df[product_col]
            .str.len() > 2
        ]

        # -------------------------------------------
        # KEEP IMPORTANT COLUMNS
        # -------------------------------------------

        clean_df = df[[
            product_col,
            "Qty"
        ]]

        clean_df.columns = [
            "Product",
            "Qty"
        ]

        # -------------------------------------------
        # SHOW CLEAN DATA
        # -------------------------------------------

        st.subheader(
            "📊 Cleaned Purchase Data"
        )

        edited_df = st.data_editor(

            clean_df,

            use_container_width=True,

            num_rows="dynamic"
        )

        # -------------------------------------------
        # METRICS
        # -------------------------------------------

        c1, c2 = st.columns(2)

        c1.metric(
            "Products",
            len(edited_df)
        )

        c2.metric(
            "Total Qty",
            int(
                edited_df["Qty"]
                .sum()
            )
        )

        # -------------------------------------------
        # SAVE BUTTON
        # -------------------------------------------

        if st.button(
            "💾 Save Purchase Data"
        ):

            # ---------------------------------------
            # SAVE CURRENT PURCHASE DATASET
            # ---------------------------------------

            edited_df.to_csv(

                purchase_dataset_path,

                index=False
            )

            # ---------------------------------------
            # UPDATE PURCHASE LEDGER
            # ---------------------------------------

            if (
                os.path.exists(ledger_path)
                and os.path.getsize(ledger_path) > 0
            ):

                old_ledger = pd.read_csv(
                    ledger_path
                )

                final_ledger = pd.concat(

                    [old_ledger, edited_df],

                    ignore_index=True
                )

            else:

                final_ledger = edited_df

            # ---------------------------------------
            # SAVE LEDGER
            # ---------------------------------------

            final_ledger.to_csv(

                ledger_path,

                index=False
            )

            # ---------------------------------------
            # LOAD INVENTORY
            # ---------------------------------------

            if (
                os.path.exists(stock_file)
                and os.path.getsize(stock_file) > 0
            ):

                stock_df = pd.read_csv(
                    stock_file
                )

            else:

                stock_df = pd.DataFrame({

                    "Product": [],

                    "Stock": []
                })

            # ---------------------------------------
            # UPDATE INVENTORY STOCK
            # ---------------------------------------

            for _, row in edited_df.iterrows():

                product = str(
                    row["Product"]
                ).strip()

                qty = int(
                    row["Qty"]
                )

                # PRODUCT EXISTS
                if product in stock_df["Product"].values:

                    stock_df.loc[
                        stock_df["Product"] == product,
                        "Stock"
                    ] += qty

                # NEW PRODUCT
                else:

                    new_row = pd.DataFrame({

                        "Product": [product],

                        "Stock": [qty]
                    })

                    stock_df = pd.concat(

                        [stock_df, new_row],

                        ignore_index=True
                    )

            # ---------------------------------------
            # SAVE INVENTORY
            # ---------------------------------------

            stock_df.to_csv(

                stock_file,

                index=False
            )

            # ---------------------------------------
            # SUCCESS MESSAGE
            # ---------------------------------------

            st.success(
                "✅ Purchase Saved & Inventory Updated"
            )

            # ---------------------------------------
            # SUMMARY
            # ---------------------------------------

            st.subheader(
                "📦 Update Summary"
            )

            s1, s2 = st.columns(2)

            s1.metric(
                "Products Updated",
                len(edited_df)
            )

            s2.metric(
                "Stock Added",
                int(
                    edited_df["Qty"]
                    .sum()
                )
            )

    except Exception as e:

        st.error(
            f"❌ Error: {e}"
        )

