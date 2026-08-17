import streamlit as st
import pandas as pd
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# SUPABASE CONNECTION
# ============================================================

try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception as e:
    st.error("Unable to connect to Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# LOAD DATA
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

    defects_response = (
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
        defects_response.data
    )

    return (
        machines,
        uptime_logs,
        maintenance_logs,
        defect_logs
    )


try:

    (
        machines,
        uptime_logs,
        maintenance_logs,
        defect_logs
    ) = load_data()

except Exception as e:

    st.error("Unable to load data from Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if machines.empty:

    st.warning("No machine data found in Supabase.")
    st.stop()


# ============================================================
# PREPARE DATA
# ============================================================

# ------------------------------------------------------------
# UPTIME
# ------------------------------------------------------------

if not uptime_logs.empty:

    uptime_logs["timestamp"] = pd.to_datetime(
        uptime_logs["timestamp"],
        errors="coerce"
    )

    # Healthy reading according to analytics_queries.sql
    uptime_logs["healthy_reading"] = (
        uptime_logs["voltage"].between(140, 200)
        &
        uptime_logs["rotation_speed"].between(300, 500)
        &
        uptime_logs["pressure"].between(80, 130)
        &
        uptime_logs["vibration"].between(25, 55)
    )

    uptime_logs["uptime_value"] = (
        uptime_logs["healthy_reading"]
        .astype(int)
        * 100
    )

else:

    uptime_logs = pd.DataFrame(
        columns=[
            "timestamp",
            "machine_id",
            "healthy_reading",
            "uptime_value"
        ]
    )


# ------------------------------------------------------------
# MACHINE UPTIME SUMMARY
# ------------------------------------------------------------

if not uptime_logs.empty:

    machine_uptime = (
        uptime_logs
        .groupby("machine_id", as_index=False)
        .agg(
            average_uptime=(
                "uptime_value",
                "mean"
            )
        )
    )

else:

    machine_uptime = pd.DataFrame(
        columns=[
            "machine_id",
            "average_uptime"
        ]
    )


# ------------------------------------------------------------
# OVERALL UPTIME
# ------------------------------------------------------------

if not uptime_logs.empty:

    overall_uptime = round(
        uptime_logs["uptime_value"].mean(),
        2
    )

else:

    overall_uptime = 0


# ------------------------------------------------------------
# DEFECT SUMMARY
# ------------------------------------------------------------

if not defect_logs.empty:

    defect_logs["timestamp"] = pd.to_datetime(
        defect_logs["timestamp"],
        errors="coerce"
    )

    defect_summary = (
        defect_logs
        .groupby("machine_id", as_index=False)
        .agg(
            total_defects=(
                "defective_units",
                "sum"
            )
        )
    )

    total_defects = int(
        defect_logs["defective_units"]
        .fillna(0)
        .sum()
    )

else:

    defect_summary = pd.DataFrame(
        columns=[
            "machine_id",
            "total_defects"
        ]
    )

    total_defects = 0


# ------------------------------------------------------------
# MAINTENANCE
# ------------------------------------------------------------

if not maintenance_logs.empty:

    maintenance_logs["timestamp"] = pd.to_datetime(
        maintenance_logs["timestamp"],
        errors="coerce"
    )

    maintenance_logs["next_due_date"] = pd.to_datetime(
        maintenance_logs["next_due_date"],
        errors="coerce"
    )

else:

    maintenance_logs = pd.DataFrame(
        columns=[
            "timestamp",
            "machine_id",
            "component",
            "log_type",
            "next_due_date"
        ]
    )


# ============================================================
# EARLY WARNING DATA
# ============================================================

warning_data = machines[
    ["machine_id", "model"]
].copy()


# Add uptime
warning_data = warning_data.merge(
    machine_uptime,
    on="machine_id",
    how="left"
)


# Add defects
warning_data = warning_data.merge(
    defect_summary,
    on="machine_id",
    how="left"
)


warning_data["average_uptime"] = (
    warning_data["average_uptime"]
    .fillna(0)
)


warning_data["total_defects"] = (
    warning_data["total_defects"]
    .fillna(0)
)


# Fleet averages
fleet_average_uptime = (
    warning_data["average_uptime"].mean()
    if not warning_data.empty
    else 0
)

fleet_average_defects = (
    warning_data["total_defects"].mean()
    if not warning_data.empty
    else 0
)


# Same rule as Pranjal's analytics query:
# LOW uptime + HIGH defects = HIGH risk

warning_data["risk_level"] = "NORMAL"

warning_data.loc[
    (
        warning_data["average_uptime"]
        < fleet_average_uptime
    )
    &
    (
        warning_data["total_defects"]
        > fleet_average_defects
    ),
    "risk_level"
] = "HIGH"


high_risk_count = int(
    (
        warning_data["risk_level"] == "HIGH"
    ).sum()
)


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
            margin-bottom:2px;
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

    st.page_link(
        "pages/machines.py",
        label="Machines",
        icon="⚙️"
    )

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

st.title("Dashboard")

st.caption(
    "SmartFactory manufacturing analytics and monitoring."
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Machines",
        len(machines)
    )


with col2:

    st.metric(
        "Average Uptime",
        f"{overall_uptime:.1f}%"
    )


with col3:

    st.metric(
        "Total Defects",
        total_defects
    )


with col4:

    st.metric(
        "High Risk Machines",
        high_risk_count
    )


st.divider()


# ============================================================
# EARLY WARNING
# ============================================================

st.subheader("⚠️ Early Warning")

st.caption(
    "Machines are marked HIGH when uptime is below the "
    "fleet average and defects are above the fleet average."
)


if not warning_data.empty:

    warning_display = warning_data[
        [
            "machine_id",
            "model",
            "average_uptime",
            "total_defects",
            "risk_level"
        ]
    ].copy()

    warning_display = warning_display.rename(
        columns={
            "machine_id": "Machine ID",
            "model": "Model",
            "average_uptime": "Average Uptime %",
            "total_defects": "Total Defects",
            "risk_level": "Risk"
        }
    )

    warning_display[
        "Average Uptime %"
    ] = warning_display[
        "Average Uptime %"
    ].round(2)

    warning_display[
        "Total Defects"
    ] = warning_display[
        "Total Defects"
    ].astype(int)

    warning_display = warning_display.sort_values(
        by=["Risk", "Average Uptime %"],
        ascending=[True, True]
    )

    st.dataframe(
        warning_display,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No warning data available."
    )


st.divider()


# ============================================================
# ANALYTICS ROW
# ============================================================

chart_col1, chart_col2 = st.columns(2)


# ============================================================
# UPTIME TREND
# ============================================================

with chart_col1:

    st.subheader("Uptime Trend")

    if not uptime_logs.empty:

        trend_data = (
            uptime_logs
            .dropna(subset=["timestamp"])
            .assign(
                log_date=lambda df:
                df["timestamp"].dt.date
            )
            .groupby("log_date")["uptime_value"]
            .mean()
            .reset_index()
        )

        trend_data = trend_data.set_index(
            "log_date"
        )

        trend_data = trend_data.rename(
            columns={
                "uptime_value": "Average Uptime %"
            }
        )

        st.line_chart(
            trend_data,
            use_container_width=True
        )

    else:

        st.info(
            "No uptime data available."
        )


# ============================================================
# DEFECTS BY MACHINE
# ============================================================

with chart_col2:

    st.subheader("Defects by Machine")

    if not defect_summary.empty:

        defects_chart = (
            defect_summary
            .merge(
                machines[
                    ["machine_id", "model"]
                ],
                on="machine_id",
                how="left"
            )
        )

        defects_chart = defects_chart[
            [
                "machine_id",
                "total_defects"
            ]
        ]

        defects_chart = defects_chart.set_index(
            "machine_id"
        )

        defects_chart = defects_chart.rename(
            columns={
                "total_defects": "Total Defects"
            }
        )

        st.bar_chart(
            defects_chart,
            use_container_width=True
        )

    else:

        st.info(
            "No defect data available."
        )


st.divider()


# ============================================================
# MAINTENANCE SUMMARY
# ============================================================

st.subheader("Recent Maintenance")

if not maintenance_logs.empty:

    maintenance_display = (
        maintenance_logs
        .sort_values(
            "timestamp",
            ascending=False
        )
        .head(5)
        .copy()
    )

    maintenance_display = maintenance_display[
        [
            "machine_id",
            "component",
            "log_type",
            "timestamp",
            "next_due_date"
        ]
    ]

    maintenance_display = maintenance_display.rename(
        columns={
            "machine_id": "Machine ID",
            "component": "Component",
            "log_type": "Type",
            "timestamp": "Date",
            "next_due_date": "Next Due"
        }
    )

    maintenance_display["Date"] = (
        pd.to_datetime(
            maintenance_display["Date"],
            errors="coerce"
        )
        .dt.strftime("%Y-%m-%d")
    )

    maintenance_display["Next Due"] = (
        pd.to_datetime(
            maintenance_display["Next Due"],
            errors="coerce"
        )
        .dt.strftime("%Y-%m-%d")
    )

    st.dataframe(
        maintenance_display,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No maintenance records available."
    )


# ============================================================
# DATA SUMMARY
# ============================================================

with st.expander("Dashboard data summary"):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write(
            f"Machines: {len(machines)}"
        )

    with col2:
        st.write(
            f"Uptime records: {len(uptime_logs)}"
        )

    with col3:
        st.write(
            f"Maintenance records: {len(maintenance_logs)}"
        )

    with col4:
        st.write(
            f"Defect records: {len(defect_logs)}"
        )