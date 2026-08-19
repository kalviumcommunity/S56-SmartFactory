import os

import pandas as pd
import streamlit as st
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory",
    page_icon=":material/monitor_heart:",
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
       DATE
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


    /* ========================================================
       TABLES
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #e4e7ec;
        border-radius: 8px;
        overflow: hidden;
        background: #ffffff;
    }


    /* ========================================================
       EXPANDERS
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

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SUPABASE
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
        raise ValueError("SUPABASE_URL is missing.")

    if not supabase_key:
        raise ValueError("SUPABASE_KEY is missing.")

    supabase = create_client(
        supabase_url,
        supabase_key,
    )

except Exception as e:

    st.error("Unable to connect to Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# DATA HELPERS
# ============================================================

def fetch_table(
    table_name,
    max_records=5000,
    batch_size=1000,
):

    records = []
    offset = 0

    while len(records) < max_records:

        response = (
            supabase
            .table(table_name)
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
        records[:max_records]
    )


def find_column(df, candidates):

    if df.empty:
        return None

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


def numeric_series(
    df,
    candidates,
):

    column = find_column(
        df,
        candidates,
    )

    if column is None:
        return pd.Series(
            dtype="float64"
        )

    return pd.to_numeric(
        df[column],
        errors="coerce",
    )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(
    ttl=300,
    show_spinner="Loading dashboard data...",
)
def load_dashboard_data():

    machines = fetch_table(
        "machines",
        max_records=1000,
    )

    defects = pd.DataFrame()

    maintenance = pd.DataFrame()

    try:
        defects = fetch_table(
            "defects",
            max_records=5000,
        )
    except Exception:
        pass

    try:
        maintenance = fetch_table(
            "maintenance_logs",
            max_records=5000,
        )
    except Exception:
        pass

    return (
        machines,
        defects,
        maintenance,
    )


try:

    machines, defects, maintenance = (
        load_dashboard_data()
    )

except Exception as e:

    st.error(
        "Unable to load dashboard data."
    )

    st.code(str(e))
    st.stop()


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
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [8, 1]
)

with header_left:

    st.title("Dashboard")

    st.caption(
        "Monitor machine performance, production quality, "
        "maintenance activity and operational risks."
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
# DASHBOARD FILTERS
# ============================================================

st.subheader(
    "Dashboard Filters"
)

filter_col1, filter_col2 = (
    st.columns([1, 2])
)


# ------------------------------------------------------------
# MODEL
# ------------------------------------------------------------

machine_model_column = find_column(
    machines,
    [
        "model",
        "machine_type",
        "type",
    ],
)

if machine_model_column:

    models = (
        machines[
            machine_model_column
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    models = (
        ["All Models"]
        + sorted(models)
    )

else:

    models = [
        "All Models"
    ]


with filter_col1:

    selected_model = st.selectbox(
        "Model",
        models,
    )


# ------------------------------------------------------------
# MACHINE
# ------------------------------------------------------------

machine_id_column = find_column(
    machines,
    [
        "machine_id",
        "id",
        "machineId",
    ],
)

if machine_id_column:

    machine_ids = (
        machines[
            machine_id_column
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    machine_ids = (
        ["All Machines"]
        + sorted(machine_ids)
    )

else:

    machine_ids = [
        "All Machines"
    ]


with filter_col2:

    selected_machine = st.selectbox(
        "Machine",
        machine_ids,
    )


# ============================================================
# FILTER MACHINES
# ============================================================

filtered_machines = machines.copy()


if (
    selected_model != "All Models"
    and machine_model_column
):

    filtered_machines = (
        filtered_machines[
            filtered_machines[
                machine_model_column
            ]
            .astype(str)
            == selected_model
        ]
    )


if (
    selected_machine != "All Machines"
    and machine_id_column
):

    filtered_machines = (
        filtered_machines[
            filtered_machines[
                machine_id_column
            ]
            .astype(str)
            == selected_machine
        ]
    )


# ============================================================
# OVERVIEW
# ============================================================

st.subheader(
    "Overview"
)


total_machines = len(
    filtered_machines
)


# ------------------------------------------------------------
# UPTIME
# ------------------------------------------------------------

uptime_values = numeric_series(
    filtered_machines,
    [
        "uptime",
        "uptime_percent",
        "uptime_percentage",
        "average_uptime",
        "avg_uptime",
    ],
)

average_uptime = (
    uptime_values.mean()
    if not uptime_values.dropna().empty
    else 0
)


# ------------------------------------------------------------
# DEFECTS
# ------------------------------------------------------------

defect_values = numeric_series(
    filtered_machines,
    [
        "total_defects",
        "defects",
        "defect_count",
    ],
)

if defect_values.dropna().empty:

    if not defects.empty:

        defect_machine_column = find_column(
            defects,
            [
                "machine_id",
                "machineId",
            ],
        )

        defect_count_column = find_column(
            defects,
            [
                "defects",
                "defect_count",
                "quantity",
                "defective_units",
                "total_defects",
            ],
        )

        if defect_count_column:

            defect_values = pd.to_numeric(
                defects[
                    defect_count_column
                ],
                errors="coerce",
            )


total_defects = (
    int(
        defect_values
        .fillna(0)
        .sum()
    )
    if not defect_values.empty
    else 0
)


# ============================================================
# HIGH-RISK MACHINES
# ============================================================

risk_uptime = (
    average_uptime
)

machine_uptime_column = find_column(
    filtered_machines,
    [
        "uptime",
        "uptime_percent",
        "uptime_percentage",
        "average_uptime",
        "avg_uptime",
    ],
)

machine_defect_column = find_column(
    filtered_machines,
    [
        "total_defects",
        "defects",
        "defect_count",
    ],
)

if (
    machine_uptime_column
    and machine_defect_column
):

    risk_df = filtered_machines.copy()

    risk_df["_uptime"] = pd.to_numeric(
        risk_df[
            machine_uptime_column
        ],
        errors="coerce",
    )

    risk_df["_defects"] = pd.to_numeric(
        risk_df[
            machine_defect_column
        ],
        errors="coerce",
    )

    uptime_average = (
        risk_df["_uptime"]
        .mean()
    )

    defect_average = (
        risk_df["_defects"]
        .mean()
    )

    high_risk_df = risk_df[
        (
            risk_df["_uptime"]
            < uptime_average
        )
        &
        (
            risk_df["_defects"]
            > defect_average
        )
    ]

else:

    high_risk_df = pd.DataFrame()


high_risk_count = len(
    high_risk_df
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = (
    st.columns(4)
)


with kpi1:

    st.metric(
        "Total Machines",
        f"{total_machines:,}",
    )


with kpi2:

    st.metric(
        "Average Uptime",
        f"{average_uptime:.1f}%",
    )


with kpi3:

    st.metric(
        "Total Defects",
        f"{total_defects:,}",
    )


with kpi4:

    st.metric(
        "High Risk Machines",
        f"{high_risk_count:,}",
    )


# ============================================================
# EARLY WARNING
# ============================================================

st.subheader(
    "Early Warning"
)

st.caption(
    "High risk indicates uptime below fleet average "
    "and defects above fleet average."
)


if not high_risk_df.empty:

    warning_display = pd.DataFrame()

    warning_display[
        "Machine ID"
    ] = (
        high_risk_df[
            machine_id_column
        ]
        .astype(str)
        .values
        if machine_id_column
        else [
            str(i + 1)
            for i in range(
                len(high_risk_df)
            )
        ]
    )

    if machine_model_column:

        warning_display[
            "Model"
        ] = (
            high_risk_df[
                machine_model_column
            ]
            .astype(str)
            .values
        )

    warning_display[
        "Average Uptime %"
    ] = high_risk_df[
        "_uptime"
    ].round(1).values

    warning_display[
        "Total Defects"
    ] = high_risk_df[
        "_defects"
    ].fillna(0).astype(int).values

    warning_display[
        "Risk"
    ] = "HIGH"

    st.dataframe(
        warning_display,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No high-risk machines detected "
        "for the current filters."
    )


# ============================================================
# ANALYTICS
# ============================================================

st.subheader(
    "Analytics"
)


chart_col1, chart_col2 = (
    st.columns(2)
)


# ------------------------------------------------------------
# UPTIME BY MACHINE
# ------------------------------------------------------------

with chart_col1:

    st.markdown(
        "**Average Uptime by Machine**"
    )

    if (
        machine_id_column
        and machine_uptime_column
        and not filtered_machines.empty
    ):

        uptime_chart = (
            filtered_machines[
                [
                    machine_id_column,
                    machine_uptime_column,
                ]
            ]
            .copy()
        )

        uptime_chart[
            machine_uptime_column
        ] = pd.to_numeric(
            uptime_chart[
                machine_uptime_column
            ],
            errors="coerce",
        )

        uptime_chart = (
            uptime_chart
            .dropna(
                subset=[
                    machine_uptime_column
                ]
            )
            .set_index(
                machine_id_column
            )
        )

        if not uptime_chart.empty:

            st.bar_chart(
                uptime_chart[
                    machine_uptime_column
                ],
                height=300,
            )

        else:

            st.info(
                "No uptime data available."
            )

    else:

        st.info(
            "No uptime data available."
        )


# ------------------------------------------------------------
# DEFECTS BY MACHINE
# ------------------------------------------------------------

with chart_col2:

    st.markdown(
        "**Defects by Machine**"
    )

    if (
        not defects.empty
        and
        find_column(
            defects,
            [
                "machine_id",
                "machineId",
            ],
        )
        and
        find_column(
            defects,
            [
                "defects",
                "defect_count",
                "quantity",
                "defective_units",
                "total_defects",
            ],
        )
    ):

        d_machine = find_column(
            defects,
            [
                "machine_id",
                "machineId",
            ],
        )

        d_value = find_column(
            defects,
            [
                "defects",
                "defect_count",
                "quantity",
                "defective_units",
                "total_defects",
            ],
        )

        defect_chart = defects.copy()

        defect_chart[
            d_value
        ] = pd.to_numeric(
            defect_chart[
                d_value
            ],
            errors="coerce",
        )

        defect_chart = (
            defect_chart
            .dropna(
                subset=[d_value]
            )
            .groupby(d_machine)[
                d_value
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
        )

        if not defect_chart.empty:

            st.bar_chart(
                defect_chart,
                height=300,
            )

        else:

            st.info(
                "No defect data available."
            )

    else:

        st.info(
            "No defect data available."
        )


# ============================================================
# MAINTENANCE SUMMARY
# ============================================================

st.subheader(
    "Maintenance Overview"
)


if not maintenance.empty:

    maintenance_type_column = find_column(
        maintenance,
        [
            "maintenance_type",
            "type",
            "log_type",
        ],
    )

    if maintenance_type_column:

        maintenance_counts = (
            maintenance[
                maintenance_type_column
            ]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )

        st.bar_chart(
            maintenance_counts,
            height=280,
        )

    else:

        st.info(
            "Maintenance type data is unavailable."
        )

else:

    st.info(
        "No maintenance data available."
    )


# ============================================================
# DATA INFORMATION
# ============================================================

with st.expander(
    "Database information"
):

    st.write(
        "Machines columns:"
    )

    st.write(
        machines.columns.tolist()
        if not machines.empty
        else []
    )

    st.write(
        "Defects columns:"
    )

    st.write(
        defects.columns.tolist()
        if not defects.empty
        else []
    )

    st.write(
        "Maintenance columns:"
    )

    st.write(
        maintenance.columns.tolist()
        if not maintenance.empty
        else []
    )