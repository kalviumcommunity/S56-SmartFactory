import importlib
import os
import sys

# Ensure root path is accessible for component imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import streamlit as st
from supabase import create_client

import components.theme
importlib.reload(components.theme)
from components.theme import apply_theme, get_theme, init_theme, render_sidebar


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory - Dashboard",
    page_icon=":material/dashboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize and apply active theme (defaults to Light)
init_theme()
apply_theme()


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

    try:
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
    except Exception:
        return all_records

    return all_records[:max_records]


# ============================================================
# LOAD DATABASE DATA
# ============================================================

@st.cache_data(
    ttl=300,
    show_spinner="Loading factory data...",
)
def load_factory_data():
    machines_data = fetch_records(
        "machines",
        max_records=1000,
    )

    maintenance_data = fetch_records(
        "maintenance_logs",
        max_records=5000,
    )

    defect_data = fetch_records(
        "defect_logs",
        max_records=5000,
    )

    machines = pd.DataFrame(machines_data)
    maintenance = pd.DataFrame(maintenance_data)
    defects = pd.DataFrame(defect_data)

    if not machines.empty and "machine_id" in machines.columns:
        machines["machine_id"] = machines["machine_id"].astype(str)

    if not defects.empty and "machine_id" in defects.columns:
        defects["machine_id"] = defects["machine_id"].astype(str)

    if not maintenance.empty and "machine_id" in maintenance.columns:
        maintenance["machine_id"] = maintenance["machine_id"].astype(str)

    return (
        machines,
        maintenance,
        defects,
    )


# ============================================================
# GET DATA
# ============================================================

try:
    (
        machines,
        maintenance,
        defects,
    ) = load_factory_data()

except Exception as e:
    st.error("Unable to load factory data from Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# HELPER TO FIND COLUMN NAMES
# ============================================================

def find_column(df, possible_names):
    if df is None or df.empty:
        return None
    for col in possible_names:
        if col in df.columns:
            return col
    return None


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

render_sidebar(current_page="dashboard")


# ============================================================
# PAGE HEADER
# ============================================================

header_left, header_right = st.columns([8, 1])

with header_left:
    st.title("Dashboard")
    st.caption(
        "Real-time operational intelligence, risk monitoring, "
        "and equipment health across the factory floor."
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
# EMPTY DATABASE CHECK
# ============================================================

if machines.empty:
    st.info("No machine records found in Supabase.")
    st.stop()


# ============================================================
# FILTER CONTROLS
# ============================================================

st.subheader("Filter Overview")

filter_col1, filter_col2 = st.columns(2)

status_column = find_column(
    machines,
    [
        "status",
        "operational_status",
        "state",
    ],
)

machine_id_column = find_column(
    machines,
    [
        "machine_id",
        "id",
    ],
)


with filter_col1:
    if status_column:
        statuses = (
            machines[status_column]
            .dropna()
            .unique()
            .tolist()
        )
        status_options = ["All Status"] + sorted(statuses)
        selected_status = st.selectbox(
            "Status",
            status_options,
        )
    else:
        selected_status = "All Status"


with filter_col2:
    if machine_id_column:
        machine_list = (
            machines[machine_id_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        machine_options = ["All Machines"] + sorted(machine_list)
        selected_machine = st.selectbox(
            "Machine",
            machine_options,
        )
    else:
        selected_machine = "All Machines"


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_machines = machines.copy()

if status_column and selected_status != "All Status":
    filtered_machines = filtered_machines[
        filtered_machines[status_column] == selected_status
    ]

if machine_id_column and selected_machine != "All Machines":
    filtered_machines = filtered_machines[
        filtered_machines[machine_id_column].astype(str) == selected_machine
    ]


# ============================================================
# METRICS COMPUTATION
# ============================================================

total_machines = len(filtered_machines)

defect_machine_col = find_column(defects, ["machine_id", "machineId"])
defect_count_col = find_column(
    defects,
    ["defect_count", "defects", "defective_units", "quantity", "count"],
)

if not defects.empty and defect_count_col:
    defects_clean = defects.copy()
    defects_clean["_count"] = pd.to_numeric(
        defects_clean[defect_count_col], errors="coerce"
    ).fillna(0)
    
    if defect_machine_col and machine_id_column:
        active_machine_ids = set(filtered_machines[machine_id_column].astype(str))
        filtered_defects = defects_clean[
            defects_clean[defect_machine_col].astype(str).isin(active_machine_ids)
        ]
        total_defects = int(filtered_defects["_count"].sum())
    else:
        filtered_defects = defects_clean
        total_defects = int(defects_clean["_count"].sum())
else:
    filtered_defects = pd.DataFrame()
    total_defects = len(defects)

uptime_col_m = find_column(
    filtered_machines,
    ["uptime", "uptime_percent", "uptime_percentage", "average_uptime", "avg_uptime"],
)

if uptime_col_m:
    average_uptime = float(
        pd.to_numeric(filtered_machines[uptime_col_m], errors="coerce")
        .dropna()
        .mean()
    )
    if pd.isna(average_uptime):
        average_uptime = 92.5
else:
    if status_column:
        operational_count = (
            filtered_machines[status_column].astype(str).str.lower() == "operational"
        ).sum()
        average_uptime = (
            float((operational_count / max(total_machines, 1)) * 100.0)
            if total_machines > 0
            else 95.0
        )
    else:
        average_uptime = 95.0


# ============================================================
# RISK MODEL
# ============================================================

if not filtered_defects.empty and defect_machine_col:
    defects_by_m = (
        filtered_defects.groupby(defect_machine_col)["_count"]
        .sum()
        .reset_index()
        .rename(columns={"_count": "total_defects"})
    )
    risk_merged = filtered_machines.merge(
        defects_by_m,
        left_on=machine_id_column,
        right_on=defect_machine_col,
        how="left",
    )
    risk_merged["total_defects"] = risk_merged["total_defects"].fillna(0)
    
    mean_defects = risk_merged["total_defects"].mean()
    
    if status_column:
        high_risk_df = risk_merged[
            (risk_merged["total_defects"] > mean_defects)
            | (risk_merged[status_column].astype(str).str.lower() != "operational")
        ]
    else:
        high_risk_df = risk_merged[risk_merged["total_defects"] > mean_defects]
else:
    if status_column:
        high_risk_df = filtered_machines[
            filtered_machines[status_column].astype(str).str.lower() != "operational"
        ]
    else:
        high_risk_df = pd.DataFrame()

high_risk_count = len(high_risk_df)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

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

st.subheader("Early Warning Indicator")

if not high_risk_df.empty:
    st.warning(
        f"{high_risk_count} machine(s) require attention "
        f"(high defect occurrences or non-operational status)."
    )

    display_cols = [
        col
        for col in [
            machine_id_column,
            find_column(filtered_machines, ["model", "type"]),
            status_column,
            find_column(high_risk_df, ["total_defects"]),
            uptime_col_m,
        ]
        if col and col in high_risk_df.columns
    ]

    st.dataframe(
        high_risk_df[display_cols],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.success("All equipment operating within normal parameters.")


# ============================================================
# ANALYTICS SECTION
# ============================================================

st.subheader("Analytics")

accent_color = "#3b82f6" if get_theme() == "dark" else "#2563eb"

chart_col1, chart_col2 = st.columns(2, gap="medium")


# ------------------------------------------------------------
# DEFECTS BY MACHINE
# ------------------------------------------------------------

with chart_col1:
    with st.container(border=True):
        st.markdown(
            """
            <div class="chart-card-title">Defects by Machine</div>
            <div class="chart-card-subtitle">Top 10 machines with highest recorded defects</div>
            """,
            unsafe_allow_html=True,
        )
        if not filtered_defects.empty and defect_machine_col:
            top_defects = (
                filtered_defects.groupby(defect_machine_col)["_count"]
                .sum()
                .rename("Defects")
                .sort_values(ascending=False)
                .head(10)
            )
            st.bar_chart(
                top_defects,
                color=accent_color,
                height=280,
            )
        else:
            st.info("No defect data available.")


# ------------------------------------------------------------
# MACHINES BY STATUS / MODEL
# ------------------------------------------------------------

with chart_col2:
    with st.container(border=True):
        if status_column:
            st.markdown(
                """
                <div class="chart-card-title">Machines by Status</div>
                <div class="chart-card-subtitle">Operational status breakdown across active assets</div>
                """,
                unsafe_allow_html=True,
            )
            status_chart = (
                filtered_machines[status_column]
                .value_counts()
                .rename("Machines")
            )
            st.bar_chart(
                status_chart,
                color=accent_color,
                height=280,
            )
        else:
            model_col = find_column(filtered_machines, ["model", "type"])
            if model_col:
                st.markdown(
                    """
                    <div class="chart-card-title">Machines by Model</div>
                    <div class="chart-card-subtitle">Equipment distribution across models</div>
                    """,
                    unsafe_allow_html=True,
                )
                model_chart = (
                    filtered_machines[model_col]
                    .value_counts()
                    .rename("Machines")
                )
                st.bar_chart(
                    model_chart,
                    color=accent_color,
                    height=280,
                )
            else:
                st.info("No categorical machine breakdown available.")


# ============================================================
# MAINTENANCE SUMMARY
# ============================================================

st.subheader("Maintenance Overview")

if not maintenance.empty:
    maint_type_col = find_column(
        maintenance,
        ["maintenance_type", "type", "log_type"],
    )

    if maint_type_col:
        with st.container(border=True):
            st.markdown(
                """
                <div class="chart-card-title">Maintenance Event Breakdown</div>
                <div class="chart-card-subtitle">Volume of preventive vs corrective service events</div>
                """,
                unsafe_allow_html=True,
            )
            maint_counts = (
                maintenance[maint_type_col]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .rename("Events")
            )
            st.bar_chart(
                maint_counts,
                color=accent_color,
                height=260,
            )
    else:
        st.info("No maintenance type classification found.")
else:
    st.info("No maintenance records found.")

st.write("")


# ============================================================
# DATABASE INFORMATION
# ============================================================

with st.expander("Database information"):
    st.write("Data sources:")
    st.code("machines\nmaintenance_logs\ndefect_logs")

    st.write("Machines columns:")
    st.write(machines.columns.tolist() if not machines.empty else [])

    st.write("Defect logs columns:")
    st.write(defects.columns.tolist() if not defects.empty else [])

    st.write("Maintenance logs columns:")
    st.write(maintenance.columns.tolist() if not maintenance.empty else [])