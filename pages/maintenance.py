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
    page_title="SmartFactory - Maintenance",
    page_icon="🔧",
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
# LOAD DATA FROM SUPABASE
# ============================================================

def fetch_records(table_name, select_cols="*", max_records=5000, batch_size=1000, order_col=None):
    """
    Fetches records from Supabase using bounded pagination for sub-second responses.
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


@st.cache_data(ttl=300, show_spinner="Loading maintenance data from Supabase...")
def load_maintenance_data():
    machines_data = fetch_records("machines", max_records=1000)
    maint_data = fetch_records("maintenance_logs", max_records=5000, order_col="timestamp" if "timestamp" else None)

    machines = pd.DataFrame(machines_data)
    maint_logs = pd.DataFrame(maint_data)

    if not machines.empty and "machine_id" in machines.columns:
        machines["machine_id"] = machines["machine_id"].astype(str)

    if not maint_logs.empty and "machine_id" in maint_logs.columns:
        maint_logs["machine_id"] = maint_logs["machine_id"].astype(str)

    return machines, maint_logs


# ============================================================
# GET DATA
# ============================================================

try:
    machines, maint_logs = load_maintenance_data()
except Exception as e:
    st.error("Unable to load maintenance data from Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# DATA PREPARATION & SCHEMA NORMALIZATION
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
            "raw_date"
        ]
    )
else:
    df = maint_logs.copy()

    # Determine date column (maintenance_date or timestamp)
    if "maintenance_date" in df.columns:
        date_col = "maintenance_date"
    elif "timestamp" in df.columns:
        date_col = "timestamp"
    else:
        date_col = None

    if date_col:
        df["raw_date"] = pd.to_datetime(df[date_col], errors="coerce")
        df["maintenance_date"] = df["raw_date"].dt.strftime("%Y-%m-%d").fillna("Not Specified")
    else:
        df["raw_date"] = pd.NaT
        df["maintenance_date"] = "Not Specified"

    # Determine type column (maintenance_type or log_type)
    if "maintenance_type" in df.columns:
        type_col = "maintenance_type"
    elif "log_type" in df.columns:
        type_col = "log_type"
    else:
        type_col = None

    if type_col:
        # Standardize 'Scheduled' -> 'Preventive', 'Failure' -> 'Corrective'
        df["maintenance_type"] = (
            df[type_col]
            .astype(str)
            .replace({"Scheduled": "Preventive", "Failure": "Corrective"})
        )
    else:
        df["maintenance_type"] = "Preventive"

    # Determine status column
    if "status" in df.columns:
        df["status"] = df["status"].fillna("Completed").astype(str)
    else:
        df["status"] = "Completed"

    # Determine maintenance_id column
    if "maintenance_id" in df.columns:
        df["maintenance_id"] = df["maintenance_id"].astype(str)
    else:
        df["maintenance_id"] = [f"MNT-{i+1:05d}" for i in range(len(df))]

    # Join model from machines
    model_col = None
    for col in ["model", "machine_type", "type"]:
        if col in machines.columns:
            model_col = col
            break

    if not machines.empty and model_col:
        machines_lookup = machines[["machine_id", model_col]].drop_duplicates(subset=["machine_id"])
        df = df.merge(machines_lookup, on="machine_id", how="left")
        df["model"] = df[model_col].fillna("Unknown")
    else:
        df["model"] = "Unknown"

    normalized_maint = df[
        [
            "maintenance_id",
            "machine_id",
            "model",
            "maintenance_date",
            "maintenance_type",
            "status",
            "raw_date"
        ]
    ].copy()


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
    st.page_link(
        "pages/maintenance.py",
        label="Maintenance",
        icon="🔧"
    )

    st.write("⚠️ Defects")
    st.write("📈 Reports")
    st.write("⬆️ Upload Data")

    st.divider()
    st.caption("Admin User")
    st.caption("admin@smartfactory.io")


# ============================================================
# PAGE HEADER
# ============================================================

st.title("Maintenance")
st.caption("Monitor scheduled preventive and corrective maintenance events across factory machinery.")
st.divider()


# ============================================================
# EMPTY DATABASE CHECK
# ============================================================

if normalized_maint.empty:
    st.info("No maintenance records found in Supabase.")
    st.stop()


# ============================================================
# FILTERS
# ============================================================

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    machine_options = ["All Machines"] + sorted(normalized_maint["machine_id"].dropna().unique().tolist())
    selected_machine = st.selectbox("Filter by Machine", machine_options)

with filter_col2:
    type_options = ["All Types"] + sorted(normalized_maint["maintenance_type"].dropna().unique().tolist())
    selected_type = st.selectbox("Maintenance Type", type_options)

with filter_col3:
    status_options = ["All Statuses"] + sorted(normalized_maint["status"].dropna().unique().tolist())
    selected_status = st.selectbox("Status", status_options)

with filter_col4:
    valid_dates = normalized_maint["raw_date"].dropna()
    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()
        selected_date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    else:
        selected_date_range = None
        st.caption("No date filters available.")


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = normalized_maint.copy()

if selected_machine != "All Machines":
    filtered_df = filtered_df[filtered_df["machine_id"] == selected_machine]

if selected_type != "All Types":
    filtered_df = filtered_df[filtered_df["maintenance_type"] == selected_type]

if selected_status != "All Statuses":
    filtered_df = filtered_df[filtered_df["status"] == selected_status]

if selected_date_range and isinstance(selected_date_range, (tuple, list)) and len(selected_date_range) == 2:
    start_d, end_d = selected_date_range
    filtered_df = filtered_df[
        (filtered_df["raw_date"].isna()) |
        ((filtered_df["raw_date"].dt.date >= start_d) & (filtered_df["raw_date"].dt.date <= end_d))
    ]

st.divider()


# ============================================================
# KPI CARDS
# ============================================================

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

total_events = len(filtered_df)
preventive_count = int((filtered_df["maintenance_type"] == "Preventive").sum())
corrective_count = int((filtered_df["maintenance_type"] == "Corrective").sum())

with kpi_col1:
    st.metric("Total Maintenance Events", f"{total_events:,}")

with kpi_col2:
    st.metric("Preventive Maintenance", f"{preventive_count:,}")

with kpi_col3:
    st.metric("Corrective / Failure Maintenance", f"{corrective_count:,}")

st.divider()


# ============================================================
# MAINTENANCE EVENTS BY TYPE CHART
# ============================================================

chart_col1, chart_col2 = st.columns([1, 1])

with chart_col1:
    st.subheader("Maintenance Events by Type")
    if not filtered_df.empty:
        type_counts = (
            filtered_df
            .groupby("maintenance_type", as_index=False)
            .agg(Total_Events=("maintenance_id", "count"))
            .rename(columns={"maintenance_type": "Type", "Total_Events": "Events"})
            .set_index("Type")
        )
        st.bar_chart(type_counts, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with chart_col2:
    st.subheader("Maintenance by Machine")
    if not filtered_df.empty:
        machine_maint_counts = (
            filtered_df
            .groupby("machine_id", as_index=False)
            .agg(Total_Events=("maintenance_id", "count"))
            .sort_values("Total_Events", ascending=False)
            .head(10)
            .rename(columns={"machine_id": "Machine ID", "Total_Events": "Events"})
            .set_index("Machine ID")
        )
        st.bar_chart(machine_maint_counts, use_container_width=True)
    else:
        st.info("No machine maintenance data available.")

st.divider()


# ============================================================
# MAINTENANCE RECORDS TABLE
# ============================================================

st.subheader("Maintenance Records")
st.caption(f"Showing {len(filtered_df):,} of {len(normalized_maint):,} maintenance logs")

display_table = filtered_df[
    [
        "maintenance_id",
        "machine_id",
        "model",
        "maintenance_date",
        "maintenance_type",
        "status"
    ]
].rename(
    columns={
        "maintenance_id": "Maintenance ID",
        "machine_id": "Machine ID",
        "model": "Model",
        "maintenance_date": "Maintenance Date",
        "maintenance_type": "Type",
        "status": "Status"
    }
)

st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True
)
