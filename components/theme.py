import os
import streamlit as st


def init_theme():
    """
    Initializes the theme in st.session_state with 'light' as the default mode.
    """
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "light"
    return st.session_state["theme_mode"]


def get_theme():
    """
    Returns the active theme mode ('light' or 'dark').
    """
    return st.session_state.get("theme_mode", "light")


def set_theme(mode):
    """
    Updates the theme mode in st.session_state.
    """
    if mode in ["light", "dark"]:
        st.session_state["theme_mode"] = mode


def apply_theme():
    """
    Injects custom CSS tailored for the currently selected theme ('light' or 'dark').
    Ensures complete visual consistency across inputs, metrics, tables, and sidebars.
    """
    theme = init_theme()

    if theme == "dark":
        css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* ========================================================
           DARK THEME TOKENS
           ======================================================== */
        :root {
            --bg-canvas: #0b0f19;
            --bg-surface: #151d2f;
            --bg-surface-elevated: #1e293b;
            --bg-surface-hover: #27354a;
            --bg-input: #151d2f;
            --border-color: #26334d;
            --border-light: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --primary-accent: #3b82f6;
            --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            --primary-light: rgba(59, 130, 246, 0.15);
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
        }

        html, body, [class*="css"], .stApp {
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        }

        .stApp {
            background-color: var(--bg-canvas) !important;
            color: var(--text-primary) !important;
        }

        .main .block-container {
            max-width: 1520px;
            padding: 28px 36px 56px 36px;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background-color: var(--bg-surface) !important;
            border-bottom: 1px solid var(--border-color) !important;
        }

        /* Typography */
        .stApp p {
            color: var(--text-secondary) !important;
            font-size: 14px;
        }

        .stApp label {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
            font-family: 'Inter', system-ui, sans-serif !important;
        }

        h1 {
            font-size: 28px !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em;
        }

        h2 {
            font-size: 19px !important;
            font-weight: 650 !important;
            letter-spacing: -0.015em;
            margin-top: 14px !important;
            margin-bottom: 8px !important;
        }

        h3 {
            font-size: 16px !important;
            font-weight: 650 !important;
            margin-top: 10px !important;
            margin-bottom: 6px !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-surface) !important;
            border-right: 1px solid var(--border-color) !important;
        }

        section[data-testid="stSidebar"] .block-container {
            padding: 24px 16px;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: var(--text-secondary) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            border-radius: 8px;
            min-height: 40px;
            margin: 4px 0;
            color: var(--text-secondary) !important;
            font-size: 13.5px;
            font-weight: 500;
            transition: all 0.15s ease-in-out;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
            background-color: var(--bg-surface-hover) !important;
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] svg {
            color: var(--text-muted) !important;
            width: 18px;
            height: 18px;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
            background-color: var(--primary-light) !important;
            color: var(--primary-accent) !important;
            font-weight: 600;
            border-left: 3px solid var(--primary-accent);
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] svg {
            color: var(--primary-accent) !important;
        }

        /* Brand Elements */
        .brand-icon {
            width: 38px;
            height: 38px;
            border-radius: 9px;
            background: var(--primary-gradient);
            color: #ffffff !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 17px;
            font-weight: 700;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
        }

        .brand-title {
            font-size: 17px;
            font-weight: 700;
            color: var(--text-primary) !important;
            line-height: 20px;
            letter-spacing: -0.02em;
        }

        .brand-subtitle {
            font-size: 11px;
            color: var(--text-muted) !important;
            margin-top: 1px;
        }

        .page-date {
            color: var(--text-muted) !important;
            font-size: 12.5px;
            text-align: right;
            padding-top: 8px;
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 18px 20px !important;
            min-height: 105px;
            box-shadow: var(--card-shadow) !important;
            position: relative;
            overflow: hidden;
            margin-bottom: 12px !important;
        }

        div[data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--primary-gradient);
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] p {
            color: var(--text-muted) !important;
            font-size: 12.5px !important;
            font-weight: 500 !important;
            letter-spacing: 0.01em;
        }

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] div {
            color: var(--text-primary) !important;
            font-size: 26px !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        /* Selectboxes & Dropdowns */
        div[data-baseweb="select"] > div {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
            min-height: 40px !important;
        }

        div[data-baseweb="select"] span {
            color: var(--text-primary) !important;
        }

        div[data-baseweb="select"] input {
            color: var(--text-primary) !important;
        }

        div[data-baseweb="select"] svg {
            fill: var(--text-muted) !important;
        }

        ul[data-baseweb="menu"],
        div[data-baseweb="popover"] {
            background-color: var(--bg-surface-elevated) !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4) !important;
        }

        ul[data-baseweb="menu"] li {
            color: var(--text-primary) !important;
            background-color: var(--bg-surface-elevated) !important;
            font-size: 13.5px !important;
        }

        ul[data-baseweb="menu"] li:hover,
        ul[data-baseweb="menu"] li[aria-selected="true"] {
            background-color: var(--bg-surface-hover) !important;
            color: var(--primary-accent) !important;
        }

        /* Date Inputs */
        div[data-testid="stDateInput"] input {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
            min-height: 40px !important;
        }

        div[data-baseweb="calendar"] {
            background-color: var(--bg-surface-elevated) !important;
            color: var(--text-primary) !important;
        }

        /* Text & Number Inputs */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
            min-height: 40px !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: var(--text-muted) !important;
        }

        /* Radios & Checkboxes */
        div[data-testid="stRadio"] label span,
        div[data-testid="stCheckbox"] label span {
            color: var(--text-primary) !important;
            font-size: 13.5px !important;
        }

        /* Dataframe / Tables */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            overflow: hidden;
            background-color: var(--bg-surface) !important;
            box-shadow: var(--card-shadow) !important;
            margin-top: 6px !important;
            margin-bottom: 16px !important;
        }

        /* Bordered Container Cards (for structured Graphs & Sections) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 18px 20px 14px 20px !important;
            box-shadow: var(--card-shadow) !important;
            margin-bottom: 16px !important;
        }

        /* Chart Canvas integration inside container */
        div[data-testid="stVegaLiteChart"],
        div[data-testid="stArrowVegaLiteChart"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        .chart-card-title {
            color: var(--text-primary) !important;
            font-size: 15px !important;
            font-weight: 650 !important;
            letter-spacing: -0.01em;
            margin-bottom: 2px !important;
        }

        .chart-card-subtitle {
            color: var(--text-muted) !important;
            font-size: 12.5px !important;
            margin-bottom: 12px !important;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            margin-top: 12px !important;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary span {
            color: var(--text-primary) !important;
            font-weight: 500 !important;
        }

        /* Alerts & Banners */
        div[data-testid="stAlert"] {
            border-radius: 10px !important;
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            margin-bottom: 14px !important;
        }

        div[data-testid="stAlert"] p {
            color: var(--text-primary) !important;
        }

        /* Captions */
        [data-testid="stCaptionContainer"] p,
        [data-testid="stCaptionContainer"] {
            color: var(--text-muted) !important;
            font-size: 12.5px !important;
        }

        /* Buttons */
        button[data-testid="stBaseButton-secondary"] {
            background-color: var(--bg-surface) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }

        button[data-testid="stBaseButton-secondary"]:hover {
            background-color: var(--bg-surface-hover) !important;
            border-color: var(--primary-accent) !important;
            color: var(--primary-accent) !important;
        }

        button[data-testid="stBaseButton-primary"] {
            background: var(--primary-gradient) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
        }

        hr {
            border-color: var(--border-color) !important;
            margin: 20px 0 !important;
        }
        </style>
        """
    else:
        # LIGHT THEME (DEFAULT)
        css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* ========================================================
           LIGHT THEME TOKENS (DEFAULT)
           ======================================================== */
        :root {
            --bg-canvas: #f8f9fb;
            --bg-surface: #ffffff;
            --bg-surface-elevated: #ffffff;
            --bg-surface-hover: #f1f5f9;
            --bg-input: #ffffff;
            --border-color: #e2e8f0;
            --border-light: #cbd5e1;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --primary-accent: #2563eb;
            --primary-gradient: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            --primary-light: #eff6ff;
            --card-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.03);
        }

        html, body, [class*="css"], .stApp {
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        }

        .stApp {
            background-color: var(--bg-canvas) !important;
            color: var(--text-primary) !important;
        }

        .main .block-container {
            max-width: 1520px;
            padding: 28px 36px 56px 36px;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background-color: var(--bg-surface) !important;
            border-bottom: 1px solid var(--border-color) !important;
        }

        /* Typography */
        .stApp p {
            color: var(--text-secondary) !important;
            font-size: 14px;
        }

        .stApp label {
            color: #1e293b !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
            font-family: 'Inter', system-ui, sans-serif !important;
        }

        h1 {
            font-size: 28px !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em;
        }

        h2 {
            font-size: 19px !important;
            font-weight: 650 !important;
            letter-spacing: -0.015em;
            margin-top: 14px !important;
            margin-bottom: 8px !important;
        }

        h3 {
            font-size: 16px !important;
            font-weight: 650 !important;
            margin-top: 10px !important;
            margin-bottom: 6px !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-surface) !important;
            border-right: 1px solid var(--border-color) !important;
        }

        section[data-testid="stSidebar"] .block-container {
            padding: 24px 16px;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: var(--text-secondary) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            border-radius: 8px;
            min-height: 40px;
            margin: 4px 0;
            color: var(--text-secondary) !important;
            font-size: 13.5px;
            font-weight: 500;
            transition: all 0.15s ease-in-out;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
            background-color: var(--bg-surface-hover) !important;
            color: var(--primary-accent) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] svg {
            color: var(--text-muted) !important;
            width: 18px;
            height: 18px;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
            background-color: var(--primary-light) !important;
            color: var(--primary-accent) !important;
            font-weight: 600;
            border-left: 3px solid var(--primary-accent);
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] svg {
            color: var(--primary-accent) !important;
        }

        /* Brand Elements */
        .brand-icon {
            width: 38px;
            height: 38px;
            border-radius: 9px;
            background: var(--primary-gradient);
            color: #ffffff !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 17px;
            font-weight: 700;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
        }

        .brand-title {
            font-size: 17px;
            font-weight: 700;
            color: var(--text-primary) !important;
            line-height: 20px;
            letter-spacing: -0.02em;
        }

        .brand-subtitle {
            font-size: 11px;
            color: var(--text-muted) !important;
            margin-top: 1px;
        }

        .page-date {
            color: var(--text-muted) !important;
            font-size: 12.5px;
            text-align: right;
            padding-top: 8px;
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 18px 20px !important;
            min-height: 105px;
            box-shadow: var(--card-shadow) !important;
            position: relative;
            overflow: hidden;
            margin-bottom: 12px !important;
        }

        div[data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--primary-gradient);
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] p {
            color: var(--text-muted) !important;
            font-size: 12.5px !important;
            font-weight: 500 !important;
            letter-spacing: 0.01em;
        }

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] div {
            color: var(--text-primary) !important;
            font-size: 26px !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        /* Selectboxes & Dropdowns */
        div[data-baseweb="select"] > div {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
            min-height: 40px !important;
        }

        div[data-baseweb="select"] span {
            color: var(--text-primary) !important;
        }

        div[data-baseweb="select"] input {
            color: var(--text-primary) !important;
        }

        ul[data-baseweb="menu"],
        div[data-baseweb="popover"] {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08) !important;
        }

        ul[data-baseweb="menu"] li {
            color: var(--text-primary) !important;
            background-color: var(--bg-surface) !important;
            font-size: 13.5px !important;
        }

        ul[data-baseweb="menu"] li:hover,
        ul[data-baseweb="menu"] li[aria-selected="true"] {
            background-color: var(--primary-light) !important;
            color: var(--primary-accent) !important;
        }

        /* Date Inputs */
        div[data-testid="stDateInput"] input {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
            min-height: 40px !important;
        }

        /* Text & Number Inputs */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
            min-height: 40px !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #94a3b8 !important;
        }

        /* Radios & Checkboxes */
        div[data-testid="stRadio"] label span,
        div[data-testid="stCheckbox"] label span {
            color: var(--text-primary) !important;
            font-size: 13.5px !important;
        }

        /* Dataframe / Tables */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            overflow: hidden;
            background-color: var(--bg-surface) !important;
            box-shadow: var(--card-shadow) !important;
            margin-top: 6px !important;
            margin-bottom: 16px !important;
        }

        /* Bordered Container Cards (for structured Graphs & Sections) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 18px 20px 14px 20px !important;
            box-shadow: var(--card-shadow) !important;
            margin-bottom: 16px !important;
        }

        /* Chart Canvas integration inside container */
        div[data-testid="stVegaLiteChart"],
        div[data-testid="stArrowVegaLiteChart"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        .chart-card-title {
            color: var(--text-primary) !important;
            font-size: 15px !important;
            font-weight: 650 !important;
            letter-spacing: -0.01em;
            margin-bottom: 2px !important;
        }

        .chart-card-subtitle {
            color: var(--text-muted) !important;
            font-size: 12.5px !important;
            margin-bottom: 12px !important;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background-color: var(--bg-surface) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            margin-top: 12px !important;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary span {
            color: var(--text-primary) !important;
            font-weight: 500 !important;
        }

        /* Alerts */
        div[data-testid="stAlert"] {
            border-radius: 10px !important;
            margin-bottom: 14px !important;
        }

        /* Captions */
        [data-testid="stCaptionContainer"] p,
        [data-testid="stCaptionContainer"] {
            color: var(--text-muted) !important;
            font-size: 12.5px !important;
        }

        /* Buttons */
        button[data-testid="stBaseButton-secondary"] {
            background-color: var(--bg-surface) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }

        button[data-testid="stBaseButton-secondary"]:hover {
            background-color: var(--bg-surface-hover) !important;
            border-color: var(--primary-accent) !important;
            color: var(--primary-accent) !important;
        }

        button[data-testid="stBaseButton-primary"] {
            background: var(--primary-gradient) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
        }

        hr {
            border-color: var(--border-color) !important;
            margin: 20px 0 !important;
        }
        </style>
        """

    st.markdown(css, unsafe_allow_html=True)


def render_sidebar(current_page=""):
    """
    Standardized sidebar navigation for SmartFactory, complete with brand banner,
    page links, and active admin profile footer.
    """
    with st.sidebar:
        brand_col1, brand_col2 = st.columns([1, 3], gap="small")

        with brand_col1:
            st.markdown(
                """
                <div class="brand-icon">
                    S
                </div>
                """,
                unsafe_allow_html=True,
            )

        with brand_col2:
            st.markdown(
                """
                <div class="brand-title">
                    SmartFactory
                </div>
                <div class="brand-subtitle">
                    Analytics Platform
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        st.caption("NAVIGATION")

        st.page_link(
            "app.py",
            label="Dashboard",
            icon=":material/dashboard:",
        )

        st.page_link(
            "pages/machines.py",
            label="Machines",
            icon=":material/precision_manufacturing:",
        )

        st.page_link(
            "pages/maintenance.py",
            label="Maintenance",
            icon=":material/build:",
        )

        if os.path.exists(os.path.join("pages", "defects.py")):
            st.page_link(
                "pages/defects.py",
                label="Defects",
                icon=":material/warning:",
            )

        if os.path.exists(os.path.join("pages", "reports.py")):
            st.page_link(
                "pages/reports.py",
                label="Reports",
                icon=":material/bar_chart:",
            )

        if os.path.exists(os.path.join("pages", "upload_data.py")):
            st.page_link(
                "pages/upload_data.py",
                label="Upload Data",
                icon=":material/upload:",
            )

        if os.path.exists(os.path.join("pages", "settings.py")):
            st.page_link(
                "pages/settings.py",
                label="Settings",
                icon=":material/settings:",
            )

        st.divider()

        st.markdown("**Admin User**")
        st.caption("admin@smartfactory.io")
