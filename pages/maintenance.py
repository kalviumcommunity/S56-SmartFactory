import os

import pandas as pd
import streamlit as st
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory - Maintenance",
    page_icon=":material/build:",
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
       GENERAL TEXT
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
       HEADER DATE
       ======================================================== */

    .page-date {
        color: #667085 !important;
        font-size: 13px;
        text-align: right;
        padding-top: 10px;
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
       DATE INPUT
       ======================================================== */

    div[data-testid="stDateInput"] label {
        color: #344054 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stDateInput"] input {
        background: #ffffff !important;
        border: 1px solid #d0d5dd !important;
        border-radius: 7px !important;
        color: #344054 !important;
    }


    /* ========================================================
       METRIC CARDS
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

    div[data-testid="stMetricDelta"] {
        color: #475467 !important;
    }


    /* ========================================================
       CHART SECTION
       ======================================================== */

    .chart-title {
        color: #101828 !important;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }


    /* ========================================================
       DATAFRAME
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
       INFO / ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 8px;
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
# PAGINATED SUPABASE FETCH
# ============================================================

def fetch_records(
    table_name,
    select_cols="*",
    max_records=5000,
    batch_size=1000,
):

    all_records = []
    offset = 0

    while len(all_records) < max_records:

        response = (
            supabase
            .table(table_name)
            .select(select_cols)
            .range(
                offset,
                offset + batch_size - 1,
            )
            .execute()
        )

        data = response.data or []

        all_records.extend(data)

        if len(data) < batch_size:
            break

        offset += batch_size

    return all_records[:max_records]


# ============================================================
# LOAD DATABASE DATA
# ============================================================

@st.cache_data(
    ttl=300,
    show_spinner="Loading maintenance data...",
)
def load_maintenance_data():

    machines_data = fetch_records(
        "machines",
        max_records=1000,
    )

    maintenance_data = fetch_records(
        "maintenance_logs",
        max_records=5000,
    )

    machines = pd.DataFrame(
        machines_data
    )

    maintenance = pd.DataFrame(
        maintenance_data
    )

    if (
        not machines.empty
        and "machine_id" in machines.columns
    ):

        machines["machine_id"] = (
            machines["machine_id"]
            .astype(str)
        )

    if (
        not maintenance.empty
        and "machine_id" in maintenance.columns
    ):

        maintenance["machine_id"] = (
            maintenance["machine_id"]
            .astype(str)
        )

    return machines, maintenance


# ============================================================
# GET DATA
# ============================================================

try:

    machines, maint_logs = (
        load_maintenance_data()
    )

except Exception as e:

    st.error(
        "Unable to load maintenance data from Supabase."
    )

    st.code(str(e))
    st.stop()


# ============================================================
# NORMALIZE MAINTENANCE DATA
# ============================================================

if maint_logs.empty:

    normalized_maint = pd.DataFrame(
        columns=[
            "maintenance_id",
            "machine_id",
            "model",
            "maintenance_date",
            "maintenance_type",
            "status",
            "raw_date",
        ]
    )

else:

    df = maint_logs.copy()

    # --------------------------------------------------------
    # DATE COLUMN
    # --------------------------------------------------------

    if "maintenance_date" in df.columns:

        date_col = "maintenance_date"

    elif "timestamp" in df.columns:

        date_col = "timestamp"

    elif "date" in df.columns:

        date_col = "date"

    else:

        date_col = None

    if date_col:

        df["raw_date"] = pd.to_datetime(
            df[date_col],
            errors="coerce",
        )

        df["maintenance_date"] = (
            df["raw_date"]
            .dt.strftime("%Y-%m-%d")
            .fillna("Not Specified")
        )

    else:

        df["raw_date"] = pd.NaT

        df["maintenance_date"] = (
            "Not Specified"
        )


    # --------------------------------------------------------
    # TYPE
    # --------------------------------------------------------

    if "maintenance_type" in df.columns:

        type_col = "maintenance_type"

    elif "log_type" in df.columns:

        type_col = "log_type"

    elif "type" in df.columns:

        type_col = "type"

    else:

        type_col = None

    if type_col:

        df["maintenance_type"] = (
            df[type_col]
            .fillna("Preventive")
            .astype(str)
        )

        df["maintenance_type"] = (
            df["maintenance_type"]
            .replace(
                {
                    "Scheduled": "Preventive",
                    "scheduled": "Preventive",
                    "Failure": "Corrective",
                    "failure": "Corrective",
                }
            )
        )

    else:

        df["maintenance_type"] = (
            "Preventive"
        )


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if "status" in df.columns:

        df["status"] = (
            df["status"]
            .fillna("Completed")
            .astype(str)
        )

    else:

        df["status"] = "Completed"


    # --------------------------------------------------------
    # MAINTENANCE ID
    # --------------------------------------------------------

    if "maintenance_id" in df.columns:

        df["maintenance_id"] = (
            df["maintenance_id"]
            .astype(str)
        )

    elif "id" in df.columns:

        df["maintenance_id"] = (
            df["id"]
            .astype(str)
        )

    else:

        df["maintenance_id"] = [
            f"MNT-{i + 1:05d}"
            for i in range(len(df))
        ]


    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model_column = None

    for column in [
        "model",
        "machine_type",
        "type",
    ]:

        if column in machines.columns:

            model_column = column
            break

    if (
        not machines.empty
        and model_column
        and "machine_id" in machines.columns
        and "machine_id" in df.columns
    ):

        machine_lookup = (
            machines[
                [
                    "machine_id",
                    model_column,
                ]
            ]
            .drop_duplicates(
                subset=["machine_id"]
            )
        )

        df = df.merge(
            machine_lookup,
            on="machine_id",
            how="left",
        )

        df["model"] = (
            df[model_column]
            .fillna("Unknown")
            .astype(str)
        )

    else:

        df["model"] = "Unknown"


    # --------------------------------------------------------
    # FINAL DATASET
    # --------------------------------------------------------

    normalized_maint = df[
        [
            "maintenance_id",
            "machine_id",
            "model",
            "maintenance_date",
            "maintenance_type",
            "status",
            "raw_date",
        ]
    ].copy()


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

    st.title("Maintenance")

    st.caption(
        "Monitor scheduled preventive and corrective "
        "maintenance events across factory machinery."
    )

with header_right:

    st.markdown(
        """
        <div class="page-date">
            """
        + pd.Timestamp.now().strftime(
            "%B %d, %Y"
        )
        + """
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# EMPTY DATABASE CHECK
# ============================================================

if normalized_maint.empty:

    st.info(
        "No maintenance records found in Supabase."
    )

    st.stop()


# ============================================================
# FILTER SECTION
# ============================================================

st.subheader(
    "Maintenance Filters"
)

filter_col1, filter_col2, filter_col3, filter_col4 = (
    st.columns(4)
)


# ------------------------------------------------------------
# MACHINE FILTER
# ------------------------------------------------------------

with filter_col1:

    machine_options = (
        normalized_maint[
            "machine_id"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    machine_options = (
        ["All Machines"]
        + sorted(machine_options)
    )

    selected_machine = st.selectbox(
        "Machine",
        machine_options,
    )


# ------------------------------------------------------------
# TYPE FILTER
# ------------------------------------------------------------

with filter_col2:

    type_options = (
        normalized_maint[
            "maintenance_type"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    type_options = (
        ["All Types"]
        + sorted(type_options)
    )

    selected_type = st.selectbox(
        "Maintenance Type",
        type_options,
    )


# ------------------------------------------------------------
# STATUS FILTER
# ------------------------------------------------------------

with filter_col3:

    status_options = (
        normalized_maint[
            "status"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    status_options = (
        ["All Statuses"]
        + sorted(status_options)
    )

    selected_status = st.selectbox(
        "Status",
        status_options,
    )


# ------------------------------------------------------------
# DATE FILTER
# ------------------------------------------------------------

with filter_col4:

    valid_dates = (
        normalized_maint[
            "raw_date"
        ]
        .dropna()
    )

    if not valid_dates.empty:

        min_date = (
            valid_dates
            .min()
            .date()
        )

        max_date = (
            valid_dates
            .max()
            .date()
        )

        selected_date_range = st.date_input(
            "Date Range",
            value=(
                min_date,
                max_date,
            ),
            min_value=min_date,
            max_value=max_date,
        )

    else:

        selected_date_range = None

        st.caption(
            "No date data available."
        )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = normalized_maint.copy()


if selected_machine != "All Machines":

    filtered_df = filtered_df[
        filtered_df[
            "machine_id"
        ].astype(str)
        == selected_machine
    ]


if selected_type != "All Types":

    filtered_df = filtered_df[
        filtered_df[
            "maintenance_type"
        ].astype(str)
        == selected_type
    ]


if selected_status != "All Statuses":

    filtered_df = filtered_df[
        filtered_df[
            "status"
        ].astype(str)
        == selected_status
    ]


if (
    selected_date_range
    and isinstance(
        selected_date_range,
        (tuple, list),
    )
    and len(selected_date_range) == 2
):

    start_date = selected_date_range[0]
    end_date = selected_date_range[1]

    date_mask = (
        filtered_df["raw_date"].isna()
        |
        (
            (
                filtered_df[
                    "raw_date"
                ].dt.date
                >= start_date
            )
            &
            (
                filtered_df[
                    "raw_date"
                ].dt.date
                <= end_date
            )
        )
    )

    filtered_df = filtered_df[
        date_mask
    ]


# ============================================================
# OVERVIEW
# ============================================================

st.subheader(
    "Overview"
)

total_events = len(
    filtered_df
)

preventive_count = int(
    (
        filtered_df[
            "maintenance_type"
        ]
        .astype(str)
        .str.lower()
        == "preventive"
    ).sum()
)

corrective_count = int(
    (
        filtered_df[
            "maintenance_type"
        ]
        .astype(str)
        .str.lower()
        == "corrective"
    ).sum()
)


kpi_col1, kpi_col2, kpi_col3 = (
    st.columns(3)
)


with kpi_col1:

    st.metric(
        "Total Maintenance Events",
        f"{total_events:,}",
    )


with kpi_col2:

    st.metric(
        "Preventive Maintenance",
        f"{preventive_count:,}",
    )


with kpi_col3:

    st.metric(
        "Corrective Maintenance",
        f"{corrective_count:,}",
    )


# ============================================================
# MAINTENANCE ANALYSIS
# ============================================================

st.subheader(
    "Maintenance Analysis"
)

chart_col1, chart_col2 = (
    st.columns(2)
)


with chart_col1:

    st.markdown(
        '<div class="chart-title">'
        'Maintenance Events by Type'
        '</div>',
        unsafe_allow_html=True,
    )

    if not filtered_df.empty:

        type_counts = (
            filtered_df
            .groupby(
                "maintenance_type"
            )
            .size()
            .rename("Events")
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            type_counts,
            height=300,
        )

    else:

        st.info(
            "No data available."
        )


with chart_col2:

    st.markdown(
        '<div class="chart-title">'
        'Maintenance by Machine'
        '</div>',
        unsafe_allow_html=True,
    )

    if not filtered_df.empty:

        machine_counts = (
            filtered_df
            .groupby(
                "machine_id"
            )
            .size()
            .rename("Events")
            .sort_values(
                ascending=False
            )
            .head(10)
        )

        st.bar_chart(
            machine_counts,
            height=300,
        )

    else:

        st.info(
            "No machine data available."
        )


# ============================================================
# MAINTENANCE RECORDS
# ============================================================

st.subheader(
    "Maintenance Records"
)

st.caption(
    f"Showing {len(filtered_df):,} "
    f"of {len(normalized_maint):,} maintenance records"
)


display_table = filtered_df[
    [
        "maintenance_id",
        "machine_id",
        "model",
        "maintenance_date",
        "maintenance_type",
        "status",
    ]
].rename(
    columns={
        "maintenance_id": "Maintenance ID",
        "machine_id": "Machine ID",
        "model": "Model",
        "maintenance_date": "Maintenance Date",
        "maintenance_type": "Type",
        "status": "Status",
    }
)


st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True,
    height=450,
)


# ============================================================
# DATABASE INFORMATION
# ============================================================

with st.expander(
    "Database information"
):

    st.write(
        "Data sources:"
    )

    st.code(
        "machines\nmaintenance_logs"
    )

    st.write(
        "Maintenance columns:"
    )

    st.write(
        (
            maint_logs.columns.tolist()
            if not maint_logs.empty
            else []
        )
    )