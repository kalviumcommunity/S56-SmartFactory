import streamlit as st
import pandas as pd
import os
from supabase import create_client
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


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
    supabase_url = st.secrets.get("SUPABASE_URL") if "SUPABASE_URL" in st.secrets else os.getenv("SUPABASE_URL")
    supabase_key = st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else os.getenv("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in st.secrets or environment variables.")
    supabase = create_client(supabase_url, supabase_key)
except Exception as e:
    st.error("Unable to connect to Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# LOAD DATA (OPTIMIZED WITH BOUNDED PAGINATION)
# ============================================================

def fetch_records(table_name, select_cols="*", max_records=5000, batch_size=1000, order_col=None):
    """
    Fetches records efficiently with bounded pagination and optional column selection
    to ensure fast sub-second dashboard loading times.
    """
    all_records = []
    offset = 0
    while len(all_records) < max_records:
        query = supabase.table(table_name).select(select_cols)
        if order_col:
            query = query.order(order_col, desc=True)
        query = query.range(offset, offset + batch_size - 1)
        response = query.execute()
        data = response.data or []
        all_records.extend(data)
        if len(data) < batch_size:
            break
        offset += batch_size
    return all_records


@st.cache_data(ttl=300, show_spinner="Loading SmartFactory data...")
def load_data():
    machines_data = fetch_records("machines", max_records=1000)
    uptime_data = fetch_records(
        "uptime_logs",
        select_cols="timestamp,machine_id,voltage,rotation_speed,pressure,vibration",
        max_records=5000,
        order_col="timestamp"
    )
    maintenance_data = fetch_records("maintenance_logs", max_records=5000, order_col="timestamp")
    defects_data = fetch_records("defect_logs", max_records=5000, order_col="timestamp")

    machines = pd.DataFrame(machines_data)
    uptime_logs = pd.DataFrame(uptime_data)
    maintenance_logs = pd.DataFrame(maintenance_data)
    defect_logs = pd.DataFrame(defects_data)

    # Standardize machine_id types for consistent joins
    for df in (machines, uptime_logs, maintenance_logs, defect_logs):
        if not df.empty and "machine_id" in df.columns:
            df["machine_id"] = df["machine_id"].astype(str)

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

    # Healthy reading thresholds according to sql/analytics_queries.sql
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
        uptime_logs["healthy_reading"].astype(int) * 100
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
else:
    defect_summary = pd.DataFrame(
        columns=[
            "machine_id",
            "total_defects"
        ]
    )


# ------------------------------------------------------------
# MAINTENANCE LOGS PREPARATION
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
# EARLY WARNING BENCHMARKS (FLEET-WIDE QUERY 9 LOGIC)
# ============================================================

warning_data = machines[
    ["machine_id", "model"]
].copy()

# Add uptime per machine
warning_data = warning_data.merge(
    machine_uptime,
    on="machine_id",
    how="left"
)

# Add defects per machine
warning_data = warning_data.merge(
    defect_summary,
    on="machine_id",
    how="left"
)

warning_data["average_uptime"] = (
    warning_data["average_uptime"].fillna(0)
)
warning_data["total_defects"] = (
    warning_data["total_defects"].fillna(0)
)

# Fleet benchmarks (Query 9 from sql/analytics_queries.sql)
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

# Rule: LOW uptime + HIGH defects = HIGH risk
warning_data["risk_level"] = "NORMAL"
warning_data.loc[
    (warning_data["average_uptime"] < fleet_average_uptime)
    &
    (warning_data["total_defects"] > fleet_average_defects),
    "risk_level"
] = "HIGH"


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
# HEADER & FILTERS
# ============================================================

st.title("Dashboard")
st.caption("SmartFactory manufacturing analytics and monitoring.")

# Interactive Filters
filter_col1, filter_col2 = st.columns([1, 2])

with filter_col1:
    available_models = ["All Models"]
    if not machines.empty and "model" in machines.columns:
        available_models += sorted(machines["model"].dropna().astype(str).unique().tolist())
    selected_model = st.selectbox("Filter by Model", available_models)

with filter_col2:
    if selected_model != "All Models":
        model_machine_ids = machines[machines["model"].astype(str) == selected_model]["machine_id"].tolist()
    else:
        model_machine_ids = machines["machine_id"].tolist()

    selected_machines = st.multiselect(
        "Filter by Machine ID",
        options=sorted(model_machine_ids),
        default=[],
        placeholder="All machines in scope (select to narrow down)..."
    )

# Determine active machines in scope
if selected_machines:
    active_machine_ids = selected_machines
elif selected_model != "All Models":
    active_machine_ids = model_machine_ids
else:
    active_machine_ids = machines["machine_id"].tolist()

# Filter active slices
active_machines = machines[machines["machine_id"].isin(active_machine_ids)]
active_uptime = uptime_logs[uptime_logs["machine_id"].isin(active_machine_ids)] if not uptime_logs.empty else uptime_logs
active_defects = defect_logs[defect_logs["machine_id"].isin(active_machine_ids)] if not defect_logs.empty else defect_logs
active_maintenance = maintenance_logs[maintenance_logs["machine_id"].isin(active_machine_ids)] if not maintenance_logs.empty else maintenance_logs
active_warning = warning_data[warning_data["machine_id"].isin(active_machine_ids)] if not warning_data.empty else warning_data

# Calculate Active KPIs
current_uptime = (
    round(active_uptime["uptime_value"].mean(), 2)
    if not active_uptime.empty
    else 0
)
current_defects = (
    int(active_defects["defective_units"].fillna(0).sum())
    if not active_defects.empty
    else 0
)
current_high_risk = int((active_warning["risk_level"] == "HIGH").sum())

st.divider()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Machines",
        len(active_machines)
    )

with col2:
    st.metric(
        "Average Uptime",
        f"{current_uptime:.1f}%"
    )

with col3:
    st.metric(
        "Total Defects",
        f"{current_defects:,}"
    )

with col4:
    st.metric(
        "High Risk Machines",
        current_high_risk
    )

st.divider()


# ============================================================
# EARLY WARNING INDICATOR (QUERY 9)
# ============================================================

st.subheader("⚠️ Early Warning")
st.caption(
    f"Fleet benchmarks — Average Uptime: {fleet_average_uptime:.1f}%, Average Defects: {fleet_average_defects:.1f}. "
    "Machines are marked HIGH when individual uptime is below fleet average AND defects are above fleet average."
)

if not active_warning.empty:
    warning_display = active_warning[
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

    warning_display["Average Uptime %"] = (
        warning_display["Average Uptime %"].round(2)
    )
    warning_display["Total Defects"] = (
        warning_display["Total Defects"].astype(int)
    )

    # Sort so HIGH risk machines appear at the top, followed by lowest uptime
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
    st.info("No warning data available for selected machines.")

st.divider()


# ============================================================
# UPTIME TREND (QUERY 3) & DEFECT ANALYTICS (QUERY 4 & 5)
# ============================================================

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Uptime Trend (Chronological)")

    if not active_uptime.empty:
        trend_data = (
            active_uptime
            .dropna(subset=["timestamp"])
            .assign(
                log_date=lambda df: df["timestamp"].dt.date
            )
            .groupby("log_date")["uptime_value"]
            .mean()
            .reset_index()
            .sort_values("log_date")  # Chronological order
        )

        trend_data = trend_data.set_index("log_date")
        trend_data = trend_data.rename(
            columns={"uptime_value": "Average Uptime %"}
        )

        st.line_chart(
            trend_data,
            use_container_width=True
        )
    else:
        st.info("No uptime data available for selected filter.")

with chart_col2:
    st.subheader("Defects by Machine")

    if not active_defects.empty:
        machine_defects_chart = (
            active_defects
            .groupby("machine_id", as_index=False)["defective_units"]
            .sum()
            .rename(columns={"defective_units": "Total Defects"})
            .sort_values("Total Defects", ascending=False)
            .set_index("machine_id")
        )

        st.bar_chart(
            machine_defects_chart,
            use_container_width=True
        )
    else:
        st.info("No defect data available for selected filter.")

st.divider()


# ============================================================
# DEFECT BREAKDOWN BY MATERIAL / TYPE (QUERY 5)
# ============================================================

st.subheader("Defect Analytics by Material / Type")

if not active_defects.empty and "material_name" in active_defects.columns:
    mat_col1, mat_col2 = st.columns([1, 1])

    material_summary = (
        active_defects
        .groupby("material_name", as_index=False)
        .agg(
            total_occurrences=("defective_units", "count"),
            total_defects=("defective_units", "sum")
        )
        .sort_values("total_defects", ascending=False)
    )

    with mat_col1:
        mat_chart_data = (
            material_summary
            .set_index("material_name")
            [["total_defects"]]
            .rename(columns={"total_defects": "Total Defective Units"})
        )
        st.bar_chart(
            mat_chart_data,
            use_container_width=True
        )

    with mat_col2:
        mat_table_display = material_summary.rename(
            columns={
                "material_name": "Defect / Material Type",
                "total_occurrences": "Incident Occurrences",
                "total_defects": "Total Defective Units"
            }
        )
        st.dataframe(
            mat_table_display,
            use_container_width=True,
            hide_index=True
        )
else:
    st.info("No material defect classification data available.")

st.divider()


# ============================================================
# MAINTENANCE SUMMARY (QUERY 6 & RECENT ACTIVITY)
# ============================================================

st.subheader("Maintenance Overview")

maint_col1, maint_col2, maint_col3 = st.columns(3)

total_maint_count = len(active_maintenance)
scheduled_count = (
    int((active_maintenance["log_type"] == "Scheduled").sum())
    if not active_maintenance.empty and "log_type" in active_maintenance.columns
    else 0
)
failure_count = (
    int((active_maintenance["log_type"] == "Failure").sum())
    if not active_maintenance.empty and "log_type" in active_maintenance.columns
    else 0
)

with maint_col1:
    st.metric("Total Maintenance Events", f"{total_maint_count:,}")

with maint_col2:
    st.metric("Scheduled (Preventive)", f"{scheduled_count:,}")

with maint_col3:
    st.metric("Failure (Corrective)", f"{failure_count:,}")

st.markdown("##### Recent Maintenance Activity")

if not active_maintenance.empty:
    maintenance_display = (
        active_maintenance
        .sort_values("timestamp", ascending=False)
        .head(10)
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
        pd.to_datetime(maintenance_display["Date"], errors="coerce")
        .dt.strftime("%Y-%m-%d")
        .fillna("—")
    )

    maintenance_display["Next Due"] = (
        pd.to_datetime(maintenance_display["Next Due"], errors="coerce")
        .dt.strftime("%Y-%m-%d")
        .fillna("Not Scheduled")
    )

    st.dataframe(
        maintenance_display,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No maintenance records available for selected filter.")


# ============================================================
# DATA SUMMARY EXPANDER
# ============================================================

with st.expander("Dashboard data summary"):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write(f"Machines in scope: {len(active_machines)} (Total: {len(machines)})")

    with col2:
        st.write(f"Uptime records: {len(active_uptime):,} (Total: {len(uptime_logs):,})")

    with col3:
        st.write(f"Maintenance records: {len(active_maintenance):,} (Total: {len(maintenance_logs):,})")

    with col4:
        st.write(f"Defect records: {len(active_defects):,} (Total: {len(defect_logs):,})")