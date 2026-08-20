import importlib
import os
import sys

# Ensure project root is in path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import streamlit as st
from supabase import create_client

import components.theme
importlib.reload(components.theme)
from components.theme import apply_theme, get_theme, init_theme, render_sidebar, set_theme

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory - Settings",
    page_icon=":material/settings:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize and apply active theme
init_theme()
apply_theme()


# ============================================================
# SUPABASE CONNECTION CHECK
# ============================================================

db_status = "Disconnected"
supabase_url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
supabase_key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
        db_status = "Connected"
    except Exception:
        db_status = "Error"
else:
    db_status = "Missing Credentials"


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar(current_page="settings")


# ============================================================
# PAGE HEADER
# ============================================================

header_left, header_right = st.columns([8, 1])

with header_left:
    st.title("Settings")
    st.caption(
        "Manage application appearance, theme preferences, "
        "operational thresholds, and database connection settings."
    )

with header_right:
    st.markdown(
        f"""
        <div class="page-date">
            {pd.Timestamp.now().strftime("%B %d, %Y")}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SECTION 1: APPEARANCE & THEME SETTINGS
# ============================================================

st.subheader("Appearance & Theme")

current_theme = get_theme()

theme_col1, theme_col2 = st.columns([2, 3], gap="medium")

with theme_col1:
    st.markdown("**Color Mode Preference**")
    st.caption(
        "Choose your preferred interface theme. "
        "Light mode is the default setting for SmartFactory."
    )

    theme_selection = st.radio(
        "Theme Mode",
        options=["Light Mode (Default)", "Dark Mode"],
        index=0 if current_theme == "light" else 1,
        label_visibility="collapsed",
    )

    target_mode = "light" if "Light" in theme_selection else "dark"

    if target_mode != current_theme:
        set_theme(target_mode)
        st.rerun()

with theme_col2:
    if current_theme == "light":
        st.markdown(
            """
            <div style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 18px 20px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
            ">
                <div style="font-weight: 700; color: #0f172a; font-size: 14.5px; margin-bottom: 4px;">
                    Light Mode
                </div>
                <div style="color: #475569; font-size: 13px; line-height: 1.5;">
                    Crisp, high-contrast light theme with clean card borders and optimal daytime readability across all factory analytics dashboards.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="
                background: #151d2f;
                border: 1px solid #26334d;
                border-radius: 12px;
                padding: 18px 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            ">
                <div style="font-weight: 700; color: #f8fafc; font-size: 14.5px; margin-bottom: 4px;">
                    Dark Mode
                </div>
                <div style="color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                    Sleek, low-glare dark theme with elevated slate surfaces and high-contrast metrics designed for control room environments.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()


# ============================================================
# SECTION 2: FACTORY & ANOMALY THRESHOLDS
# ============================================================

st.subheader("Factory Health & Alert Thresholds")
st.caption(
    "Set benchmark thresholds used by the Early Warning indicator "
    "and risk analytics engine."
)

thresh_col1, thresh_col2, thresh_col3 = st.columns(3)

with thresh_col1:
    uptime_warning = st.slider(
        "Uptime Warning Threshold (%)",
        min_value=50,
        max_value=99,
        value=st.session_state.get("thresh_uptime_warn", 85),
        step=1,
        help="Machines below this uptime percentage trigger operational warnings.",
    )
    st.session_state["thresh_uptime_warn"] = uptime_warning

with thresh_col2:
    uptime_critical = st.slider(
        "Uptime Critical Threshold (%)",
        min_value=40,
        max_value=90,
        value=st.session_state.get("thresh_uptime_crit", 75),
        step=1,
        help="Machines below this uptime percentage are flagged as High Risk.",
    )
    st.session_state["thresh_uptime_crit"] = uptime_critical

with thresh_col3:
    defect_threshold = st.slider(
        "Defect Rate Alert Threshold (%)",
        min_value=1.0,
        max_value=20.0,
        value=float(st.session_state.get("thresh_defect_rate", 5.0)),
        step=0.5,
        help="Defect rates exceeding this value are highlighted in quality reports.",
    )
    st.session_state["thresh_defect_rate"] = defect_threshold

st.divider()


# ============================================================
# SECTION 3: DATABASE & CACHE MANAGEMENT
# ============================================================

st.subheader("Database & System Management")

db_col1, db_col2 = st.columns(2)

with db_col1:
    st.markdown("**Supabase Connection Status**")
    if db_status == "Connected":
        st.success("Connected to Supabase PostgreSQL Database", icon=":material/check_circle:")
    else:
        st.error(f"Database Status: {db_status}", icon=":material/error:")

    masked_url = (
        supabase_url[:18] + "..." + supabase_url[-12:]
        if supabase_url and len(supabase_url) > 30
        else "Configured via environment"
    )
    st.caption(f"Endpoint: `{masked_url}`")

with db_col2:
    st.markdown("**Application Cache**")
    st.caption(
        "Clear cached Supabase queries to immediately reload the newest records "
        "across Dashboard, Machines, Maintenance, and Defects pages."
    )

    if st.button("Clear Application Cache", type="secondary", icon=":material/refresh:"):
        st.cache_data.clear()
        st.toast("Application cache cleared successfully!", icon="✅")

st.divider()


# ============================================================
# SECTION 4: USER PROFILE & ACCESS
# ============================================================

st.subheader("User Profile")

prof_col1, prof_col2 = st.columns(2)

with prof_col1:
    st.text_input("Current User", value="Admin User", disabled=True)
    st.text_input("Role", value="Operations Administrator", disabled=True)

with prof_col2:
    st.text_input("Email", value="admin@smartfactory.io", disabled=True)
    st.text_input("Permissions", value="Full Access (Read, Filter, Export)", disabled=True)
