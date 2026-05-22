import streamlit as st

def metric_card(title, value, emoji):

    st.markdown(f'''

    <div class="metric-card">

    <h3>{emoji} {title}</h3>

    <h1>{value}</h1>

    </div>

    ''', unsafe_allow_html=True)