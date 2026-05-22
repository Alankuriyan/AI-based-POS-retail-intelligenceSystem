import streamlit as st
import joblib

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="sales oracle",
    page_icon=".",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# HIDE SIDEBAR COMPLETELY
# ---------------------------------------------------

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD MODEL (SAFE)
# ---------------------------------------------------

MODEL_PATH = "models/retail_model.pkl"
DATA_PATH = "models/processed_data.pkl"
META_PATH = "models/metadata.pkl"

if "model" not in st.session_state:
    try:
        st.session_state["model"] = joblib.load(MODEL_PATH)
        st.session_state["data"] = joblib.load(DATA_PATH)

        metadata = joblib.load(META_PATH)

        st.session_state["prod_col"] = metadata["prod_col"]
        st.session_state["date_col"] = metadata["date_col"]
        st.session_state["qty_col"] = metadata["qty_col"]
        st.session_state["price_col"] = metadata["price_col"]
        st.session_state["features"] = metadata["features"]

        st.session_state["model_loaded"] = True

    except:
        st.session_state["model_loaded"] = False

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div style="
    padding:50px;
    border-radius:20px;
    background:linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
    text-align:center;
">
    <h1 style="font-size:50px;">sales oracle</h1>
    <p style="font-size:18px; opacity:0.8;">
        POS System • Inventory • AI Forecasting • Analytics
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# MODEL STATUS
# ---------------------------------------------------

if st.session_state.get("model_loaded"):
    st.success("✅ AI Model Loaded Successfully")
else:
    st.warning("⚠ Model Not Loaded")

# ---------------------------------------------------
# NAVIGATION
# ---------------------------------------------------

st.markdown("##  Choose System")

c1, c2, c3 = st.columns(3)

# ---------------- POS ----------------

with c1:
    st.markdown("""
    <div style="
        padding:20px;
        border-radius:15px;
        background:#111827;
        color:white;
        border:1px solid #2d3748;
    ">
        <h3>🛒 POS SYSTEM</h3>
        <p>Billing & Sales Entry System</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open POS", use_container_width=True):
        st.switch_page("pages/10_POS_System.py")

# ---------------- AI ----------------

with c2:
    st.markdown("""
    <div style="
        padding:20px;
        border-radius:15px;
        background:#111827;
        color:white;
        border:1px solid #2d3748;
    ">
        <h3>🤖 AI ANALYTICS</h3>
        <p>Forecasting & Insights</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open AI Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

# ---------------- INVENTORY ----------------

with c3:
    st.markdown("""
    <div style="
        padding:20px;
        border-radius:15px;
        background:#111827;
        color:white;
        border:1px solid #2d3748;
    ">
        <h3>📦 INVENTORY</h3>
        <p>Stock Management System</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Inventory", use_container_width=True):
        st.switch_page("pages/9_Manage_Inventory.py")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<br><br>
<div style="text-align:center; opacity:0.5;">
Minix AI Retail System • Built with Streamlit
</div>
""", unsafe_allow_html=True)