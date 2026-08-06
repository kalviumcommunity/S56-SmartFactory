import streamlit as st

st.set_page_config(
    page_title="SmartFactory",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 SmartFactory")

st.write(
    "Manufacturing analytics dashboard for monitoring "
    "machine uptime, maintenance, and production defects."
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Machines", "20")

with col2:
    st.metric("Average Uptime", "94%")

with col3:
    st.metric("Total Defects", "32")

with col4:
    st.metric("Maintenance Due", "4")

st.info("Dashboard setup completed. Data integration will be added later.")