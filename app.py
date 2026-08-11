import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SUPABASE CONNECTION
# ============================================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f8fa;
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    h1 {
        color: #172033;
        font-size: 28px;
        font-weight: 700;
    }

    h2, h3 {
        color: #172033;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280;
    }

    div[data-testid="stMetricValue"] {
        color: #172033;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA FROM SUPABASE
# ============================================================

@st.cache_data(ttl=300)
def load_data():

    machines_response = (
        supabase
        .table("machines")
        .select("*")
        .execute()
    )

    uptime_response = (
        supabase
        .table("uptime_logs")
        .select("*")
        .execute()
    )

    maintenance_response = (
        supabase
        .table("maintenance_logs")
        .select("*")
        .execute()
    )

    defect_response = (
        supabase
        .table("defect_logs")
        .select("*")
        .execute()
    )

    machines = pd.DataFrame(
        machines_response.data
    )

    uptime_logs = pd.DataFrame(
        uptime_response.data
    )

    maintenance_logs = pd.DataFrame(
        maintenance_response.data
    )

    defect_logs = pd.DataFrame(
        defect_response.data
    )

    return (
        machines,
        uptime_logs,
        maintenance_logs,
        defect_logs
    )


# ============================================================
# GET DATA
# ============================================================

try:

    (
        machines,
        uptime_logs,
        maintenance_logs,
        defect_logs
    ) = load_data()

except Exception as e:

    st.error(
        "Unable to load data from Supabase."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# CONVERT DATE COLUMNS
# ============================================================

if "log_date" in uptime_logs.columns:

    uptime_logs["log_date"] = pd.to_datetime(
        uptime_logs["log_date"],
        errors="coerce"
    )


if "maintenance_date" in maintenance_logs.columns:

    maintenance_logs["maintenance_date"] = pd.to_datetime(
        maintenance_logs["maintenance_date"],
        errors="coerce"
    )


if "log_date" in defect_logs.columns:

    defect_logs["log_date"] = pd.to_datetime(
        defect_logs["log_date"],
        errors="coerce"
    )


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_machines = (
    machines["machine_id"].nunique()
    if "machine_id" in machines.columns
    else 0
)


average_uptime = (
    uptime_logs["uptime_percentage"].mean()
    if "uptime_percentage" in uptime_logs.columns
    and not uptime_logs.empty
    else 0
)


total_defects = (
    defect_logs["defect_count"].sum()
    if "defect_count" in defect_logs.columns
    and not defect_logs.empty
    else 0
)


if (
    "status" in maintenance_logs.columns
    and not maintenance_logs.empty
):

    maintenance_due = maintenance_logs[
        maintenance_logs["status"]
        .astype(str)
        .str.lower()
        .isin(
            [
                "pending",
                "scheduled",
                "due"
            ]
        )
    ].shape[0]

else:

    maintenance_due = 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:700;
            color:#172033;
        ">
            ⚡ SmartFactory
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Analytics Platform")

    st.divider()

    st.markdown("**NAVIGATION**")

    st.page_link(
        "app.py",
        label="Dashboard",
        icon="📊"
    )

    st.write("⚙️ Machines")

    st.write("🔧 Maintenance")

    st.write("⚠️ Defects")

    st.write("📈 Reports")

    st.write("⬆️ Upload Data")

    st.divider()

    st.caption("Admin User")
    st.caption("admin@smartfactory.io")


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2 = st.columns(
    [5, 1]
)


with header_col1:

    st.title("Dashboard")

    st.caption(
        "Monitor machine performance, maintenance activity "
        "and production defects."
    )


with header_col2:

    st.write("")

    st.caption(
        pd.Timestamp.today().strftime(
            "%B %d, %Y"
        )
    )


st.divider()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Machines",
        f"{total_machines:,}"
    )

    st.caption(
        "Machines currently monitored"
    )


with col2:

    st.metric(
        "Average Uptime",
        f"{average_uptime:.1f}%"
    )

    st.caption(
        "Average machine uptime"
    )


with col3:

    st.metric(
        "Total Defects",
        f"{int(total_defects):,}"
    )

    st.caption(
        "Recorded defects"
    )


with col4:

    st.metric(
        "Maintenance Due",
        f"{maintenance_due:,}"
    )

    st.caption(
        "Pending or scheduled"
    )


st.write("")


# ============================================================
# CHARTS
# ============================================================

chart_left, chart_right = st.columns(
    [2, 1]
)


# ============================================================
# UPTIME TREND
# ============================================================

with chart_left:

    st.subheader("Uptime Trend")

    st.caption(
        "Machine uptime performance over time"
    )

    if (
        "log_date" in uptime_logs.columns
        and "uptime_percentage" in uptime_logs.columns
        and not uptime_logs.empty
    ):

        fig_uptime = px.line(
            uptime_logs,
            x="log_date",
            y="uptime_percentage",
            color="machine_id",
            markers=True
        )

        fig_uptime.update_layout(
            height=360,
            xaxis_title="Date",
            yaxis_title="Uptime (%)",
            legend_title="Machine",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            fig_uptime,
            use_container_width=True
        )

    else:

        st.info(
            "No uptime data available."
        )


# ============================================================
# DEFECTS BY MACHINE
# ============================================================

with chart_right:

    st.subheader("Defects by Machine")

    st.caption(
        "Total recorded defects"
    )

    if (
        "machine_id" in defect_logs.columns
        and "defect_count" in defect_logs.columns
        and not defect_logs.empty
    ):

        defect_summary = (
            defect_logs
            .groupby(
                "machine_id",
                as_index=False
            )["defect_count"]
            .sum()
            .sort_values(
                "defect_count",
                ascending=False
            )
        )

        fig_defects = px.bar(
            defect_summary,
            x="machine_id",
            y="defect_count"
        )

        fig_defects.update_layout(
            height=360,
            xaxis_title="Machine",
            yaxis_title="Defects",
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            fig_defects,
            use_container_width=True
        )

    else:

        st.info(
            "No defect data available."
        )


# ============================================================
# RECENT MAINTENANCE
# ============================================================

st.subheader("Recent Maintenance")

st.caption(
    "Latest maintenance service events"
)


if not maintenance_logs.empty:

    recent_maintenance = (
        maintenance_logs
        .sort_values(
            by="maintenance_date",
            ascending=False
        )
        .head(5)
        .copy()
    )

    if "maintenance_date" in recent_maintenance.columns:

        recent_maintenance[
            "maintenance_date"
        ] = recent_maintenance[
            "maintenance_date"
        ].dt.strftime(
            "%Y-%m-%d"
        )

    display_columns = [
        "maintenance_id",
        "machine_id",
        "maintenance_date",
        "maintenance_type",
        "status"
    ]

    display_columns = [
        column
        for column in display_columns
        if column in recent_maintenance.columns
    ]

    st.dataframe(
        recent_maintenance[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No maintenance records available."
    )


# ===========================================================
# FOOTER
# ===========================================================

st.divider()

st.caption(
    "SmartFactory | Manufacturing Quality Analytics"
)