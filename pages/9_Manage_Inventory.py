import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.title("📦 Manage Inventory")

st.info(
    "📡 Inventory is connected to Purchase Uploads"
)

# ---------------------------------------------------
# CHECK DATA
# ---------------------------------------------------

if "data" not in st.session_state:

    st.warning("⚠ Train model first")
    st.stop()

# ---------------------------------------------------
# GET DATA
# ---------------------------------------------------

data = st.session_state["data"]
prod_col = st.session_state["prod_col"]

products = sorted(
    data[prod_col].astype(str).unique()
)

# ---------------------------------------------------
# INVENTORY FILE
# ---------------------------------------------------

os.makedirs("inventory", exist_ok=True)
stock_file = "inventory/stock_data.csv"

# ---------------------------------------------------
# LOAD STOCK SAFELY
# ---------------------------------------------------

if (
    os.path.exists(stock_file)
    and os.path.getsize(stock_file) > 0
):

    stock_df = pd.read_csv(stock_file)

else:

    stock_df = pd.DataFrame({
        "Product": products,
        "Stock": 0
    })

    stock_df.to_csv(stock_file, index=False)

# ---------------------------------------------------
# ADD MISSING PRODUCTS
# ---------------------------------------------------

existing_products = stock_df["Product"].astype(str).tolist()

missing_products = [
    p for p in products if p not in existing_products
]

if missing_products:

    new_df = pd.DataFrame({
        "Product": missing_products,
        "Stock": 0
    })

    stock_df = pd.concat([stock_df, new_df], ignore_index=True)

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

total_products = len(stock_df)
total_stock = stock_df["Stock"].sum()
low_stock = len(stock_df[stock_df["Stock"] < 10])

c1, c2, c3 = st.columns(3)

c1.metric("📦 Products", total_products)
c2.metric("🛒 Total Stock", int(total_stock))
c3.metric("⚠ Low Stock", low_stock)

# ---------------------------------------------------
# LAST UPDATED
# ---------------------------------------------------

if os.path.exists(stock_file):

    updated_time = datetime.fromtimestamp(
        os.path.getmtime(stock_file)
    )

    st.caption(
        f"🕒 Last Inventory Update: {updated_time.strftime('%d-%m-%Y %H:%M:%S')}"
    )

# ---------------------------------------------------
# SAVE CSV INVENTORY
# ---------------------------------------------------

if st.button("💾 Save Inventory (CSV)"):

    pd.DataFrame(
        st.session_state.get("updated_stock", stock_df.to_dict("records"))
    ).to_csv(stock_file, index=False)

    st.success("✅ Inventory Saved to CSV")

# ---------------------------------------------------
# POSTGRESQL SAVE (NEW)
# ---------------------------------------------------

st.markdown("---")
st.subheader("🗄️ Database Backup")

if st.button("💾 Save Inventory to PostgreSQL"):

    try:
        from db import get_connection

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory_snapshot (
                product TEXT,
                stock INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # clear old snapshot
        cur.execute("DELETE FROM inventory_snapshot")

        # insert fresh data
        for _, row in stock_df.iterrows():
            cur.execute("""
                INSERT INTO inventory_snapshot (product, stock)
                VALUES (%s, %s)
            """, (row["Product"], int(row["Stock"])))

        conn.commit()
        cur.close()
        conn.close()

        st.success("✅ Inventory saved to PostgreSQL!")

    except Exception as e:
        st.error(f"❌ Database error: {e}")

# ---------------------------------------------------
# ADD PRODUCT
# ---------------------------------------------------

with st.expander("➕ Add New Product", expanded=False):

    new_product = st.text_input("Product Name")
    new_stock = st.number_input("Initial Stock", min_value=0, step=1)

    if st.button("Add Product"):

        if new_product.strip():

            new_row = pd.DataFrame({
                "Product": [new_product],
                "Stock": [new_stock]
            })

            stock_df = pd.concat([stock_df, new_row], ignore_index=True)
            stock_df.to_csv(stock_file, index=False)

            st.success("✅ Product Added")
            st.rerun()

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

search = st.text_input("🔍 Search Product")

if search:
    stock_df = stock_df[
        stock_df["Product"].astype(str).str.contains(search, case=False)
    ]

# ---------------------------------------------------
# SESSION STATE UPDATE
# ---------------------------------------------------

if "updated_stock" not in st.session_state:
    st.session_state["updated_stock"] = []

st.session_state["updated_stock"] = []

# ---------------------------------------------------
# GRID UI
# ---------------------------------------------------

cols = st.columns(4)

for idx, row in stock_df.iterrows():

    col = cols[idx % 4]

    with col:

        current_stock = int(row["Stock"])

        if current_stock <= 5:
            status = "🔴 Critical"
            border_color = "#ef4444"

        elif current_stock <= 15:
            status = "🟠 Low"
            border_color = "#f59e0b"

        else:
            status = "🟢 Healthy"
            border_color = "#22c55e"

        st.markdown(
            f"""
            <div style='padding:10px;border:2px solid {border_color};
            border-radius:10px;margin-bottom:10px;'>
            <h4>{row["Product"]}</h4>
            <p>{status}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        stock = st.number_input(
            "Stock",
            min_value=0,
            value=current_stock,
            step=1,
            key=f"stock_{idx}"
        )

        st.session_state["updated_stock"].append({
            "Product": row["Product"],
            "Stock": stock
        })