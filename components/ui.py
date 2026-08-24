import streamlit as st

def inject_global_ui():
    st.markdown(
        """
        <style>
        .stApp { background: #f8f9fb; color: #101828; }
        .main .block-container { max-width: 1500px; padding: 32px 40px 60px; }
        h1, h2, h3, h4 { color: #101828 !important; }
        p, label { color: #475467 !important; }
        div[data-testid="stMetric"] {
            background: #fff;
            border: 1px solid #e4e7ec;
            border-radius: 10px;
            box-shadow: 0 1px 2px rgba(16,24,40,.03);
        }
        div[data-testid="stMetricValue"] { color: #101828 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
