import os

import pandas as pd
import streamlit as st
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory - Machines",
    page_icon=":material/precision_manufacturing:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       BASE
       ======================================================== */

    .stApp {
        background: #f8f9fb;
        color: #101828;
    }

    .main .block-container {
        max-width: 1500px;
        padding: 32px 40px 60px 40px;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: #ffffff;
        border-bottom: 1px solid #eaecf0;
    }


    /* ========================================================
       TEXT
       ======================================================== */

    .stApp p {
        color: #475467 !important;
    }

    .stApp label {
        color: #344054 !important;
    }

    h1,
    h2,
    h3,
    h4 {
        color: #101828 !important;
    }

    h1 {
        font-size: 30px !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
    }

    h2 {
        font-size: 20px !important;
        font-weight: 650 !important;
    }

    h3 {
        font-size: 18px !important;
        font-weight: 650 !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e4e7ec;
    }

    section[data-testid="stSidebar"] .block-container {
        padding: 24px 16px;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #344054 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stPageLink-NavLink"] {
        border-radius: 8px;
        min-height: 42px;
        margin: 4px 0;
        color: #344054 !important;
        font-size: 14px;
        font-weight: 500;
    }

    section[data-testid="stSidebar"]
    [data-testid="stPageLink-NavLink"]:hover {
        background: #f2f5ff;
        color: #2563eb !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stPageLink-NavLink"] svg {
        color: #475467 !important;
        width: 19px;
        height: 19px;
    }

    section[data-testid="stSidebar"]
    [data-testid="stPageLink-NavLink"][aria-current="page"] {
        background: #edf3ff;
        color: #2563eb !important;
        font-weight: 600;
    }

    section[data-testid="stSidebar"]
    [data-testid="stPageLink-NavLink"][aria-current="page"] svg {
        color: #2563eb !important;
    }


    /* ========================================================
       BRAND
       ======================================================== */

    .brand-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: #2563eb;
        color: #ffffff !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 700;
    }

    .brand-title {
        font-size: 18px;
        font-weight: 700;
        color: #101828 !important;
        line-height: 22px;
    }

    .brand-subtitle {
        font-size: 11px;
        color: #667085 !important;
        margin-top: 2px;
    }


    /* ========================================================
       FILTERS
       ======================================================== */

    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #d0d5dd !important;
        border-radius: 7px !important;
        color: #344054 !important;
    }

    div[data-baseweb="select"] span {
        color: #344054 !important;
    }

    div[data-baseweb="select"] input {
        color: #344054 !important;
    }

    ul[data-baseweb="menu"] {
        background: #ffffff !important;
    }

    ul[data-baseweb="menu"] li {
        color: #344054 !important;
        background: #ffffff !important;
    }

    ul[data-baseweb="menu"] li:hover {
        background: #f2f4f7 !important;
    }

    div[data-testid="stSelectbox"] label {
        color: #344054 !important;
        font-weight: 600 !important;
    }


    /* ========================================================
       SEARCH
       ======================================================== */

    div[data-testid="stTextInput"] label {
        color: #344054 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stTextInput"] input {
        background: #ffffff !important;
        border: 1px solid #d0d5dd !important;
        border-radius: 7px !important;
        color: #344054 !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #98a2b3 !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #e4e7ec !important;
        border-radius: 10px !important;
        padding: 18px !important;
        min-height: 105px;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);
    }

    div[data-testid="stMetricLabel"] {
        color: #667085 !important;
        font-size: 12px !important;
    }

    div[data-testid="stMetricLabel"] p {
        color: #667085 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #101828 !important;
        font-size: 27px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricValue"] div {
        color: #101828 !important;
    }


    /* ========================================================
       TABLE
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #e4e7ec;
        border-radius: 8px;
        overflow: hidden;
        background: #ffffff;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #e4e7ec !important;
        border-radius: 8px !important;
    }

    [data-testid="stExpander"] summary {
        color: #344054 !important;
    }

    [data-testid="stExpander"] summary span {
        color: #344054 !important;
    }


    /* ========================================================
       CAPTIONS
       ======================================================== */

    [data-testid="stCaptionContainer"] {
        color: #667085 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #667085 !important;
    }


    /* ========================================================
       PAGE DATE
       ======================================================== */

    .page-date {
        color: #667085 !important;
        font-size: 13px;
        text-align: right;
        padding-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SUPABASE CONNECTION
# ============================================================

try:

    if "SUPABASE_URL" in st.secrets:
        supabase_url = st.secrets["SUPABASE_URL"]
    else:
        supabase_url = os.getenv("SUPABASE_URL")

    if "SUPABASE_KEY" in st.secrets:
        supabase_key = st.secrets["SUPABASE_KEY"]
    else:
        supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url:
        raise ValueError(
            "SUPABASE_URL is missing."
        )

    if not supabase_key:
        raise ValueError(
            "SUPABASE_KEY is missing."
        )

    supabase = create_client(
        supabase_url,
        supabase_key,
    )

except Exception as e:

    st.error(
        "Unable to connect to Supabase."
    )

    st.code(str(e))
    st.stop()


# ============================================================
# LOAD MACHINES
# ============================================================

@st.cache_data(
    ttl=300,
    show_spinner="Loading machine data...",
)
def load_machines():

    records = []
    offset = 0
    batch_size = 1000

    while len(records) < 5000:

        response = (
            supabase
            .table("machines")
            .select("*")
            .range(
                offset,
                offset + batch_size - 1,
            )
            .execute()
        )

        batch = response.data or []

        records.extend(batch)

        if len(batch) < batch_size:
            break

        offset += batch_size

    return pd.DataFrame(
        records[:5000]
    )


# ============================================================
# GET DATA
# ============================================================

try:

    machines = load_machines()

except Exception as e:

    st.error(
        "Unable to load machine data from Supabase."
    )

    st.code(str(e))
    st.stop()


# ============================================================
# COLUMN HELPERS
# ============================================================

def find_column(
    df,
    candidates,
):

    lower_map = {
        str(column).lower(): column
        for column in df.columns
    }

    for candidate in candidates:

        if candidate.lower() in lower_map:

            return lower_map[
                candidate.lower()
            ]

    return None


machine_id_column = find_column(
    machines,
    [
        "machine_id",
        "machineId",
        "id",
    ],
)

model_column = find_column(
    machines,
    [
        "model",
        "machine_type",
        "type",
    ],
)

status_column = find_column(
    machines,
    [
        "status",
        "machine_status",
    ],
)

uptime_column = find_column(
    machines,
    [
        "uptime",
        "uptime_percent",
        "uptime_percentage",
        "average_uptime",
        "avg_uptime",
    ],
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    brand_col1, brand_col2 = st.columns(
        [1, 3],
        gap="small",
    )

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

    if os.path.exists(
        os.path.join(
            "pages",
            "defects.py",
        )
    ):

        st.page_link(
            "pages/defects.py",
            label="Defects",
            icon=":material/warning:",
        )

    if os.path.exists(
        os.path.join(
            "pages",
            "reports.py",
        )
    ):

        st.page_link(
            "pages/reports.py",
            label="Reports",
            icon=":material/bar_chart:",
        )

    if os.path.exists(
        os.path.join(
            "pages",
            "upload_data.py",
        )
    ):

        st.page_link(
            "pages/upload_data.py",
            label="Upload Data",
            icon=":material/upload:",
        )

    st.divider()

    st.markdown(
        "**Admin User**"
    )

    st.caption(
        "admin@smartfactory.io"
    )


# ============================================================
# PAGE HEADER
# ============================================================

header_left, header_right = st.columns(
    [8, 1]
)

with header_left:

    st.title("Machines")

    st.caption(
        "View and filter machines stored "
        "in the SmartFactory database."
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
# EMPTY DATA CHECK
# ============================================================

if machines.empty:

    st.info(
        "No machine records found in Supabase."
    )

    st.stop()


# ============================================================
# SEARCH + MODEL FILTER
# ============================================================

search_col, model_col = (
    st.columns([2, 1])
)


with search_col:

    search = st.text_input(
        "Search",
        placeholder=(
            "Search machine ID, model "
            "or other information..."
        ),
    )


with model_col:

    if model_column:

        model_options = (
            machines[
                model_column
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        model_options = (
            ["All"]
            + sorted(model_options)
        )

    else:

        model_options = [
            "All"
        ]

    selected_model = st.selectbox(
        "Model / Type",
        model_options,
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_machines = (
    machines.copy()
)


# ------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------

if search:

    search_text = (
        search
        .strip()
        .lower()
    )

    if search_text:

        mask = (
            filtered_machines
            .astype(str)
            .apply(
                lambda column:
                column.str.lower()
                .str.contains(
                    search_text,
                    na=False,
                )
            )
            .any(axis=1)
        )

        filtered_machines = (
            filtered_machines[
                mask
            ]
        )


# ------------------------------------------------------------
# MODEL
# ------------------------------------------------------------

if (
    selected_model != "All"
    and model_column
):

    filtered_machines = (
        filtered_machines[
            filtered_machines[
                model_column
            ]
            .astype(str)
            == selected_model
        ]
    )


# ============================================================
# OVERVIEW METRICS
# ============================================================

st.subheader(
    "Overview"
)


machine_count = len(
    filtered_machines
)

database_count = len(
    machines
)


if status_column:

    status_values = (
        filtered_machines[
            status_column
        ]
        .fillna("")
        .astype(str)
        .str.lower()
    )

    running_count = int(
        status_values.isin(
            [
                "running",
                "active",
                "online",
            ]
        ).sum()
    )

else:

    running_count = 0


kpi1, kpi2, kpi3 = (
    st.columns(3)
)


with kpi1:

    st.metric(
        "Machines",
        f"{machine_count:,}",
    )


with kpi2:

    st.metric(
        "Records in Database",
        f"{database_count:,}",
    )


with kpi3:

    st.metric(
        "Running Machines",
        f"{running_count:,}",
    )


# ============================================================
# RESULT COUNT
# ============================================================

st.caption(
    f"Showing {len(filtered_machines):,} "
    f"of {len(machines):,} machines"
)


# ============================================================
# MACHINE RECORDS
# ============================================================

st.subheader(
    "Machine Records"
)

st.caption(
    "Live data from the Supabase machines table."
)


# ============================================================
# BUILD DISPLAY TABLE SAFELY
# ============================================================

display_data = pd.DataFrame(
    index=filtered_machines.index
)


# Machine ID

if machine_id_column:

    display_data[
        "Machine ID"
    ] = filtered_machines[
        machine_id_column
    ].astype(str)

else:

    display_data[
        "Machine ID"
    ] = filtered_machines.index.astype(str)


# Model

if model_column:

    display_data[
        "Model"
    ] = filtered_machines[
        model_column
    ].fillna(
        "Unknown"
    ).astype(str)

else:

    display_data[
        "Model"
    ] = "Unknown"


# Status

if status_column:

    display_data[
        "Status"
    ] = filtered_machines[
        status_column
    ].fillna(
        "Unknown"
    ).astype(str)

else:

    display_data[
        "Status"
    ] = "Unknown"


# Uptime if available

if uptime_column:

    uptime_values = pd.to_numeric(
        filtered_machines[
            uptime_column
        ],
        errors="coerce",
    )

    display_data[
        "Uptime %"
    ] = uptime_values.round(1)


# ============================================================
# DISPLAY
# ============================================================

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True,
    height=500,
)


# ============================================================
# DATABASE INFORMATION
# ============================================================

with st.expander(
    "Database information"
):

    st.write(
        "Columns available in the Supabase "
        "machines table:"
    )

    st.write(
        machines.columns.tolist()
    )