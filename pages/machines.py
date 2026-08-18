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
    page_title="SmartFactory - Machines",
    page_icon="⚙️",
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
# LOAD MACHINES FROM SUPABASE
# ============================================================

@st.cache_data(ttl=300)
def load_machines():

    response = (
        supabase
        .table("machines")
        .select("*")
        .execute()
    )

    return pd.DataFrame(response.data)


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
# PAGE HEADER
# ============================================================

st.title("Machines")

st.caption(
    "View machines stored in the SmartFactory database."
)

st.divider()


# ============================================================
# EMPTY DATABASE CHECK
# ============================================================

if machines.empty:

    st.info("No machine records found in Supabase.")
    st.stop()


# ============================================================
# SEARCH
# ============================================================

search = st.text_input(
    "Search",
    placeholder="Search machine information..."
)


# ============================================================
# MACHINE TYPE / MODEL FILTER
# ============================================================

machine_type_column = None

possible_type_columns = [
    "model",
    "machine_type",
    "type",
    "machineType"
]

for column in possible_type_columns:

    if column in machines.columns:

        machine_type_column = column
        break


if machine_type_column:

    machine_types = ["All"] + sorted(
        machines[machine_type_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    filter_label = "Machine Model" if machine_type_column == "model" else "Machine Type"
    selected_type = st.selectbox(
        filter_label,
        machine_types
    )

else:

    selected_type = "All"


# ============================================================
# FILTER DATA
# ============================================================

filtered_machines = machines.copy()


# Search across every column
if search:

    search_text = search.strip().lower()

    mask = filtered_machines.apply(
        lambda row: row.astype(str)
        .str.lower()
        .str.contains(
            search_text,
            na=False
        )
        .any(),
        axis=1
    )

    filtered_machines = filtered_machines[mask]


# Machine type filter
if (
    machine_type_column
    and selected_type != "All"
):

    filtered_machines = filtered_machines[
        filtered_machines[
            machine_type_column
        ].astype(str)
        == selected_type
    ]


# ============================================================
# RESULT COUNT
# ============================================================

st.caption(
    f"Showing {len(filtered_machines)} "
    f"of {len(machines)} machines"
)


# ============================================================
# DISPLAY TABLE
# ============================================================

st.dataframe(
    filtered_machines,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DATABASE INFORMATION
# ============================================================

with st.expander("Database information"):

    st.write(
        "Columns available in the Supabase machines table:"
    )

    st.write(
        machines.columns.tolist()
    )