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
    page_title="SmartFactory - Defects",
    page_icon=":material/warning:",
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
    show_spinner="Loading defect data...",
)
def load_defect_data():
    machines_data = fetch_records(
        "machines",
        max_records=1000,
    )

    defect_data = fetch_records(
        "defect_logs",
        max_records=5000,
    )

    machines_df = pd.DataFrame(machines_data)
    defects_df = pd.DataFrame(defect_data)

    if (
        not machines_df.empty
        and "machine_id" in machines_df.columns
    ):
        machines_df["machine_id"] = (
            machines_df["machine_id"].astype(str)
        )

    if (
        not defects_df.empty
        and "machine_id" in defects_df.columns
    ):
        defects_df["machine_id"] = (
            defects_df["machine_id"].astype(str)
        )

    return machines_df, defects_df


# ============================================================
# GET DATA
# ============================================================

try:
    machines, raw_defects = load_defect_data()
except Exception as e:
    st.error("Unable to load defect data from Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# NORMALIZE DEFECT DATA
# ============================================================

if raw_defects.empty:
    normalized_defects = pd.DataFrame(
        columns=[
            "defect_id",
            "machine_id",
            "model",
            "log_date",
            "defect_count",
            "defect_type",
            "raw_date",
        ]
    )
else:
    df = raw_defects.copy()

    # --------------------------------------------------------
    # DATE COLUMN
    # --------------------------------------------------------
    date_col = None
    for candidate in ["log_date", "timestamp", "date", "datetime"]:
        if candidate in df.columns:
            date_col = candidate
            break

    if date_col:
        df["raw_date"] = pd.to_datetime(
            df[date_col],
            errors="coerce",
        )
        df["log_date"] = (
            df["raw_date"]
            .dt.strftime("%Y-%m-%d")
            .fillna("Not Specified")
        )
    else:
        df["raw_date"] = pd.NaT
        df["log_date"] = "Not Specified"

    # --------------------------------------------------------
    # DEFECT COUNT
    # --------------------------------------------------------
    count_col = None
    for candidate in [
        "defect_count",
        "defective_units",
        "defects",
        "defect_units",
        "count",
    ]:
        if candidate in df.columns:
            count_col = candidate
            break

    if count_col:
        df["defect_count"] = (
            pd.to_numeric(df[count_col], errors="coerce")
            .fillna(0)
            .round()
            .astype(int)
        )
    elif "production_output" in df.columns and "defect_rate" in df.columns:
        output_series = pd.to_numeric(
            df["production_output"], errors="coerce"
        ).fillna(0)
        rate_series = pd.to_numeric(
            df["defect_rate"], errors="coerce"
        ).fillna(0)
        df["defect_count"] = (
            (output_series * rate_series / 100.0)
            .round()
            .astype(int)
        )
    else:
        df["defect_count"] = 1

    # --------------------------------------------------------
    # DEFECT TYPE (HANDLE MISSING / NULL SAFELY)
    # --------------------------------------------------------
    type_col = None
    for candidate in [
        "defect_type",
        "material_name",
        "type",
        "classification",
        "category",
    ]:
        if candidate in df.columns:
            type_col = candidate
            break

    if type_col:
        df["defect_type"] = (
            df[type_col]
            .fillna("Unclassified")
            .astype(str)
            .str.strip()
        )
        df["defect_type"] = df["defect_type"].replace(
            {
                "": "Unclassified",
                "nan": "Unclassified",
                "None": "Unclassified",
                "null": "Unclassified",
            }
        )
    else:
        df["defect_type"] = "Unclassified"

    # --------------------------------------------------------
    # DEFECT ID
    # --------------------------------------------------------
    id_col = None
    for candidate in ["defect_id", "id"]:
        if candidate in df.columns:
            id_col = candidate
            break

    if id_col:
        df["defect_id"] = df[id_col].astype(str)
    else:
        df["defect_id"] = [
            f"DEF-{i + 1:05d}" for i in range(len(df))
        ]

    # --------------------------------------------------------
    # MODEL LOOKUP FROM MACHINES
    # --------------------------------------------------------
    model_column = None
    for column in ["model", "machine_type", "type"]:
        if not machines.empty and column in machines.columns:
            model_column = column
            break

    if (
        not machines.empty
        and model_column
        and "machine_id" in machines.columns
        and "machine_id" in df.columns
    ):
        machine_lookup = (
            machines[["machine_id", model_column]]
            .drop_duplicates(subset=["machine_id"])
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
    # FINAL NORMALIZED DATASET
    # --------------------------------------------------------
    normalized_defects = df[
        [
            "defect_id",
            "machine_id",
            "model",
            "log_date",
            "defect_count",
            "defect_type",
            "raw_date",
        ]
    ].copy()


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar(current_page="defects")


# ============================================================
# PAGE HEADER
# ============================================================

header_left, header_right = st.columns([8, 1])

with header_left:
    st.title("Defects")
    st.caption(
        "Monitor defect occurrences, track quality trends, "
        "and isolate high-defect machinery across the factory floor."
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

if normalized_defects.empty:
    st.info("No defect records found in Supabase.")
    st.stop()


# ============================================================
# FILTER SECTION
# ============================================================

st.subheader("Defect Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)


# ------------------------------------------------------------
# MACHINE FILTER
# ------------------------------------------------------------

with filter_col1:
    machine_options = (
        normalized_defects["machine_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    machine_options = ["All Machines"] + sorted(machine_options)
    selected_machine = st.selectbox(
        "Machine",
        machine_options,
    )


# ------------------------------------------------------------
# DEFECT TYPE FILTER
# ------------------------------------------------------------

with filter_col2:
    type_options = (
        normalized_defects["defect_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    type_options = ["All Defect Types"] + sorted(type_options)
    selected_type = st.selectbox(
        "Defect Type",
        type_options,
    )


# ------------------------------------------------------------
# DATE RANGE FILTER
# ------------------------------------------------------------

with filter_col3:
    valid_dates = normalized_defects["raw_date"].dropna()

    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        selected_date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    else:
        selected_date_range = None
        st.caption("No date data available.")


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = normalized_defects.copy()

if selected_machine != "All Machines":
    filtered_df = filtered_df[
        filtered_df["machine_id"].astype(str) == selected_machine
    ]

if selected_type != "All Defect Types":
    filtered_df = filtered_df[
        filtered_df["defect_type"].astype(str) == selected_type
    ]

if (
    selected_date_range
    and isinstance(selected_date_range, (tuple, list))
    and len(selected_date_range) == 2
):
    start_date = selected_date_range[0]
    end_date = selected_date_range[1]

    date_mask = (
        filtered_df["raw_date"].isna()
        | (
            (filtered_df["raw_date"].dt.date >= start_date)
            & (filtered_df["raw_date"].dt.date <= end_date)
        )
    )
    filtered_df = filtered_df[date_mask]


# ============================================================
# OVERVIEW KPIS (Requirement 1)
# ============================================================

st.subheader("Overview")

total_defects = int(filtered_df["defect_count"].sum())
machines_with_defects = int(
    filtered_df[filtered_df["defect_count"] > 0]["machine_id"].nunique()
    if not filtered_df.empty
    else 0
)
defect_types_count = int(
    filtered_df["defect_type"].nunique()
    if not filtered_df.empty
    else 0
)

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric(
        "Total Defects",
        f"{total_defects:,}",
    )

with kpi_col2:
    st.metric(
        "Machines with Defects",
        f"{machines_with_defects:,}",
    )

with kpi_col3:
    st.metric(
        "Defect Types",
        f"{defect_types_count:,}",
    )


# ============================================================
# ANALYTICS (Requirement 3 & 7: Query 4, Query 5, Trend)
# ============================================================

st.subheader("Defect Analytics")

accent_color = "#3b82f6" if get_theme() == "dark" else "#2563eb"

chart_col1, chart_col2 = st.columns(2, gap="medium")

# ------------------------------------------------------------
# DEFECTS BY MACHINE (Query 4)
# ------------------------------------------------------------

with chart_col1:
    with st.container(border=True):
        st.markdown(
            """
            <div class="chart-card-title">Defects by Machine</div>
            <div class="chart-card-subtitle">Top 10 machines with highest defect counts</div>
            """,
            unsafe_allow_html=True,
        )
        if not filtered_df.empty:
            machine_defect_series = (
                filtered_df.groupby("machine_id")["defect_count"]
                .sum()
                .rename("Defects")
                .sort_values(ascending=False)
                .head(10)
            )
            st.bar_chart(
                machine_defect_series,
                color=accent_color,
                height=280,
            )
        else:
            st.info("No defect data available.")


# ------------------------------------------------------------
# DEFECTS BY DEFECT TYPE (Query 5)
# ------------------------------------------------------------

with chart_col2:
    with st.container(border=True):
        st.markdown(
            """
            <div class="chart-card-title">Defects by Defect Type</div>
            <div class="chart-card-subtitle">Top defect classifications across all machinery</div>
            """,
            unsafe_allow_html=True,
        )
        if not filtered_df.empty:
            type_defect_series = (
                filtered_df.groupby("defect_type")["defect_count"]
                .sum()
                .rename("Defects")
                .sort_values(ascending=False)
                .head(10)
            )
            st.bar_chart(
                type_defect_series,
                color=accent_color,
                height=280,
            )
        else:
            st.info("No defect type data available.")


# ------------------------------------------------------------
# DEFECT TREND OVER TIME
# ------------------------------------------------------------

with st.container(border=True):
    st.markdown(
        """
        <div class="chart-card-title">Defect Trend Over Time</div>
        <div class="chart-card-subtitle">Daily defect occurrences timeline across the factory floor</div>
        """,
        unsafe_allow_html=True,
    )

    if not filtered_df.empty and not filtered_df["raw_date"].dropna().empty:
        trend_series = (
            filtered_df.dropna(subset=["raw_date"])
            .groupby(filtered_df["raw_date"].dt.date)["defect_count"]
            .sum()
            .rename("Defects")
            .sort_index()
        )
        st.line_chart(
            trend_series,
            color=accent_color,
            height=260,
        )
    else:
        st.info("No date-based defect trends available.")

st.write("")


# ============================================================
# DETAILED DEFECT RECORDS TABLE (Requirement 4)
# ============================================================

st.subheader("Defect Records")

st.caption(
    f"Showing {len(filtered_df):,} "
    f"of {len(normalized_defects):,} defect records"
)

display_table = filtered_df[
    [
        "defect_id",
        "machine_id",
        "model",
        "log_date",
        "defect_count",
        "defect_type",
    ]
].rename(
    columns={
        "defect_id": "Defect ID",
        "machine_id": "Machine ID",
        "model": "Model",
        "log_date": "Log Date",
        "defect_count": "Defect Count",
        "defect_type": "Defect Type",
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

with st.expander("Database information"):
    st.write("Data sources:")
    st.code("machines\ndefect_logs")

    st.write("Defect logs columns:")
    st.write(
        raw_defects.columns.tolist()
        if not raw_defects.empty
        else []
    )
