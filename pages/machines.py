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
    page_title="SmartFactory - Machines",
    page_icon=":material/precision_manufacturing:",
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

    try:
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
    except Exception:
        return pd.DataFrame(records)

    return pd.DataFrame(records[:5000])


# ============================================================
# GET DATA
# ============================================================

try:
    machines = load_machines()
except Exception as e:
    st.error("Unable to load machine data from Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# COLUMN HELPERS
# ============================================================

def find_column(df, candidates):
    if df is None or df.empty:
        return None
    lower_map = {str(c).lower().strip(): c for c in df.columns}
    for candidate in candidates:
        candidate_lower = candidate.lower().strip()
        if candidate_lower in lower_map:
            return lower_map[candidate_lower]
    return None


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar(current_page="machines")


# ============================================================
# PAGE HEADER
# ============================================================

header_left, header_right = st.columns([8, 1])

with header_left:
    st.title("Machines")
    st.caption(
        "Explore factory asset registry, operational statuses, "
        "and equipment specifications across production lines."
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
# IDENTIFY KEY COLUMNS
# ============================================================

machine_id_col = find_column(
    machines,
    ["machine_id", "machineid", "id", "machine_code"],
)

status_col = find_column(
    machines,
    ["status", "operational_status", "state", "machine_status"],
)

model_col = find_column(
    machines,
    ["model", "machine_type", "type", "equipment_type"],
)

age_col = find_column(
    machines,
    ["age_years", "age", "years_in_service", "machine_age"],
)


# ============================================================
# FILTERS & SEARCH
# ============================================================

st.subheader("Filter & Search")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    search_query = st.text_input(
        "Search Machine ID / Model",
        placeholder="e.g. M01 or CNC...",
    ).strip()

with filter_col2:
    if status_col:
        status_values = (
            machines[status_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        status_choices = ["All Statuses"] + sorted(status_values)
        selected_status = st.selectbox(
            "Status",
            status_choices,
        )
    else:
        selected_status = "All Statuses"

with filter_col3:
    if model_col:
        model_values = (
            machines[model_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        model_choices = ["All Models"] + sorted(model_values)
        selected_model = st.selectbox(
            "Model",
            model_choices,
        )
    else:
        selected_model = "All Models"


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = machines.copy()

if search_query:
    search_conditions = pd.Series([False] * len(filtered_df), index=filtered_df.index)
    if machine_id_col:
        search_conditions |= (
            filtered_df[machine_id_col]
            .astype(str)
            .str.contains(search_query, case=False, na=False)
        )
    if model_col:
        search_conditions |= (
            filtered_df[model_col]
            .astype(str)
            .str.contains(search_query, case=False, na=False)
        )
    filtered_df = filtered_df[search_conditions]

if status_col and selected_status != "All Statuses":
    filtered_df = filtered_df[
        filtered_df[status_col].astype(str) == selected_status
    ]

if model_col and selected_model != "All Models":
    filtered_df = filtered_df[
        filtered_df[model_col].astype(str) == selected_model
    ]


# ============================================================
# SUMMARY METRICS
# ============================================================

st.subheader("Overview")

total_count = len(filtered_df)

if status_col:
    operational_count = int(
        (
            filtered_df[status_col]
            .astype(str)
            .str.lower()
            == "operational"
        ).sum()
    )
    maintenance_count = int(
        (
            filtered_df[status_col]
            .astype(str)
            .str.lower()
            .str.contains("maint|repair|offline", regex=True)
        ).sum()
    )
else:
    operational_count = total_count
    maintenance_count = 0

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        "Total Machines",
        f"{total_count:,}",
    )

with metric_col2:
    st.metric(
        "Operational",
        f"{operational_count:,}",
    )

with metric_col3:
    st.metric(
        "Under Maintenance / Offline",
        f"{maintenance_count:,}",
    )


# ============================================================
# MACHINE DIRECTORY TABLE
# ============================================================

st.subheader("Machine Registry")

st.caption(
    f"Showing {len(filtered_df):,} of {len(machines):,} total machines"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    height=450,
)


# ============================================================
# DATABASE INFO
# ============================================================

with st.expander("Database information"):
    st.write("Data sources:")
    st.code("machines")
    st.write("Columns:")
    st.write(machines.columns.tolist() if not machines.empty else [])