# pages/upload_data.py

import os
from datetime import datetime

import pandas as pd
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

from components.theme import render_sidebar


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory - Upload Data",
    page_icon=":material/upload:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CUSTOM STYLES
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       SMARTFACTORY BRAND
       ======================================================== */

    .brand-icon {
        width: 38px !important;
        height: 38px !important;
        border-radius: 9px !important;
        background: var(--primary-accent, #3b82f6) !important;
        color: #ffffff !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25) !important;
    }


    /* ========================================================
       PAGE LAYOUT
       ======================================================== */

    .sf-page-header {
        padding-top: 4px;
        padding-bottom: 18px;
        border-bottom: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
        margin-bottom: 26px;
    }

    .sf-page-header h1 {
        color: var(--text-primary, inherit);
        font-size: 30px;
        font-weight: 700;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
    }

    .sf-page-header p {
        color: var(--text-secondary, inherit);
        opacity: 0.75;
        font-size: 13.5px;
        margin: 0;
    }


    /* ========================================================
       UPLOAD CARDS
       ======================================================== */

    .sf-upload-card {
        border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
        border-radius: 14px;
        padding: 20px;
        min-height: 145px;
        background: var(--bg-surface, rgba(255, 255, 255, 0.05));
        margin-bottom: 12px;
        box-sizing: border-box;
    }

    .sf-upload-card h3 {
        margin: 12px 0 8px 0;
        color: var(--text-primary, inherit);
        font-size: 17px;
        font-weight: 700;
    }

    .sf-upload-card p {
        color: var(--text-secondary, inherit);
        opacity: 0.75;
        font-size: 13px;
        line-height: 1.5;
        margin: 0;
    }

    .sf-upload-icon {
        width: 42px;
        height: 42px;
        border-radius: 10px;
        background: var(--primary-light, rgba(59, 130, 246, 0.15));
        color: var(--primary-accent, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 21px;
        font-weight: 700;
    }


    /* ========================================================
       FILE INFO
       ======================================================== */

    .sf-file-info {
        color: var(--text-secondary, inherit);
        opacity: 0.7;
        font-size: 12px;
        margin-top: 5px;
    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .sf-section-title {
        color: var(--text-primary, inherit);
        font-size: 22px;
        font-weight: 700;
        margin-top: 12px;
        margin-bottom: 6px;
    }

    .sf-section-caption {
        color: var(--text-secondary, inherit);
        opacity: 0.7;
        font-size: 13px;
        margin-bottom: 18px;
    }


    /* ========================================================
       UPLOAD HISTORY
       ======================================================== */

    .sf-history-card {
        border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
        border-radius: 12px;
        padding: 14px 16px;
        background: var(--bg-surface, rgba(255, 255, 255, 0.05));
        margin-bottom: 10px;
    }

    .sf-history-title {
        color: var(--text-primary, inherit);
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .sf-history-meta {
        color: var(--text-secondary, inherit);
        opacity: 0.7;
        font-size: 12px;
    }


    /* ========================================================
       SUPPORTED FORMAT BOX
       ======================================================== */

    .sf-format-box {
        border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
        border-radius: 12px;
        padding: 18px;
        background: var(--bg-surface, rgba(255, 255, 255, 0.05));
    }

    .sf-format-box h4 {
        color: var(--text-primary, inherit);
        margin: 12px 0 8px 0;
        font-size: 15px;
        font-weight: 600;
    }

    .sf-format-box h4:first-child {
        margin-top: 0;
    }

    .sf-format-box p,
    .sf-format-box li {
        color: var(--text-secondary, inherit);
        opacity: 0.8;
        font-size: 13px;
        line-height: 1.6;
    }


    /* ========================================================
       STREAMLIT FILE UPLOADER
       ======================================================== */

    div[data-testid="stFileUploader"] {
        border-radius: 10px;
    }

    div[data-testid="stFileUploader"] section {
        background: var(--bg-surface, rgba(255, 255, 255, 0.05)) !important;
        border: 1px dashed var(--border-color, rgba(255, 255, 255, 0.2)) !important;
        border-radius: 10px !important;
    }


    /* ========================================================
       DATA PREVIEW
       ======================================================== */

    .sf-preview-title {
        color: var(--text-primary, inherit);
        font-size: 15px;
        font-weight: 650;
        margin-top: 12px;
        margin-bottom: 8px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {
        .sf-page-header h1 {
            font-size: 25px;
        }

        .sf-upload-card {
            min-height: auto;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar(current_page="upload_data")


# ============================================================
# SUPABASE CONNECTION
# ============================================================

def get_supabase_client():
    """
    Create a Supabase client using Streamlit secrets first,
    then environment variables.
    """

    try:
        supabase_url = st.secrets.get("SUPABASE_URL")
        supabase_key = st.secrets.get("SUPABASE_KEY")
    except Exception:
        supabase_url = None
        supabase_key = None

    if not supabase_url:
        supabase_url = os.getenv("SUPABASE_URL")

    if not supabase_key:
        supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url:
        raise ValueError("SUPABASE_URL is missing.")

    if not supabase_key:
        raise ValueError("SUPABASE_KEY is missing.")

    return create_client(
        supabase_url,
        supabase_key,
    )


# ============================================================
# INITIALIZE SUPABASE
# ============================================================

try:
    supabase = get_supabase_client()
except Exception as e:
    st.error("Unable to connect to Supabase.")
    st.code(str(e))
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "upload_history" not in st.session_state:
    st.session_state.upload_history = []


# ============================================================
# DATABASE TABLE CONFIGURATION
# ============================================================

UPLOAD_CONFIG = {
    "uptime": {
        "title": "Machine Uptime CSV",
        "description": (
            "Upload machine telemetry and uptime records."
        ),
        "icon": "↕",
        "table": "uptime_logs",
        "columns": [
            "timestamp",
            "machine_id",
            "voltage",
            "rotation_speed",
            "pressure",
            "vibration",
            "is_running",
        ],
        "aliases": {
            "datetime": "timestamp",
            "machineID": "machine_id",
            "machine_id": "machine_id",
            "volt": "voltage",
            "rotate": "rotation_speed",
        },
    },

    "maintenance": {
        "title": "Maintenance Records CSV",
        "description": (
            "Upload scheduled maintenance and failure records."
        ),
        "icon": "↗",
        "table": "maintenance_logs",
        "columns": [
            "timestamp",
            "machine_id",
            "component",
            "log_type",
            "next_due_date",
        ],
        "aliases": {
            "datetime": "timestamp",
            "machineID": "machine_id",
            "comp": "component",
            "failure": "component",
        },
    },

    "defects": {
        "title": "Defect Records CSV",
        "description": (
            "Upload production output and manufacturing defect records."
        ),
        "icon": "!",
        "table": "defect_logs",
        "columns": [
            "timestamp",
            "machine_id",
            "material_name",
            "production_output",
            "defect_rate",
            "defective_units",
            "energy_consumed",
        ],
        "aliases": {
            "Timestamp": "timestamp",
            "Machine ID": "machine_id",
            "Material Name": "material_name",
            "Production Output (Units)": "production_output",
            "Defect Rate (%)": "defect_rate",
            "Energy Consumption (kWh)": "energy_consumed",
        },
    },
}


# ============================================================
# DATA PREPARATION
# ============================================================

def normalize_columns(df, aliases):
    """
    Rename known source column names into SmartFactory
    database column names.
    """

    rename_map = {}

    for source_column in df.columns:
        if source_column in aliases:
            rename_map[source_column] = aliases[source_column]

    if rename_map:
        df = df.rename(columns=rename_map)

    return df


def prepare_dataframe(df, upload_type):
    """
    Normalize and prepare an uploaded DataFrame according
    to the selected SmartFactory table.
    """

    config = UPLOAD_CONFIG[upload_type]

    df = df.copy()

    # Normalize column names.
    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    df = normalize_columns(
        df,
        config["aliases"],
    )

    # Remove completely empty rows.
    df = df.dropna(
        how="all"
    ).reset_index(
        drop=True
    )

    # Machine IDs are stored as strings.
    if "machine_id" in df.columns:
        df["machine_id"] = (
            df["machine_id"]
            .astype(str)
            .replace(
                {"nan": None}
            )
        )

    # Defect logs:
    # Calculate defective_units if it was not supplied.
    if upload_type == "defects":

        if (
            "defective_units" not in df.columns
            and "production_output" in df.columns
            and "defect_rate" in df.columns
        ):
            production_output = pd.to_numeric(
                df["production_output"],
                errors="coerce",
            )

            defect_rate = pd.to_numeric(
                df["defect_rate"],
                errors="coerce",
            )

            df["defective_units"] = (
                production_output
                * defect_rate
                / 100.0
            ).round()

        if "defective_units" in df.columns:
            df["defective_units"] = pd.to_numeric(
                df["defective_units"],
                errors="coerce",
            )

    # Convert numeric columns where appropriate.
    numeric_columns = [
        "voltage",
        "rotation_speed",
        "pressure",
        "vibration",
        "production_output",
        "defect_rate",
        "defective_units",
        "energy_consumed",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    # Convert boolean values for uptime.
    if "is_running" in df.columns:

        def convert_boolean(value):
            if pd.isna(value):
                return None

            if isinstance(value, bool):
                return value

            value = str(value).strip().lower()

            if value in {
                "true",
                "1",
                "yes",
                "y",
                "running",
            }:
                return True

            if value in {
                "false",
                "0",
                "no",
                "n",
                "stopped",
            }:
                return False

            return None

        df["is_running"] = df["is_running"].apply(
            convert_boolean
        )

    return df


# ============================================================
# VALIDATION
# ============================================================

def validate_dataframe(df, upload_type):
    """
    Validate uploaded CSV against the selected table.
    """

    config = UPLOAD_CONFIG[upload_type]

    required_columns = config["columns"]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    errors = []

    if missing_columns:
        errors.append(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    if df.empty:
        errors.append(
            "The uploaded CSV contains no data rows."
        )

    if "machine_id" in df.columns:
        empty_machine_ids = (
            df["machine_id"]
            .isna()
            .sum()
        )

        if empty_machine_ids > 0:
            errors.append(
                f"{empty_machine_ids} row(s) have an empty machine_id."
            )

    if "timestamp" in df.columns:
        parsed_dates = pd.to_datetime(
            df["timestamp"],
            errors="coerce",
        )

        invalid_dates = (
            parsed_dates.isna().sum()
        )

        if invalid_dates > 0:
            errors.append(
                f"{invalid_dates} row(s) contain invalid timestamps."
            )

    if "defect_rate" in df.columns:
        defect_rate = pd.to_numeric(
            df["defect_rate"],
            errors="coerce",
        )

        invalid_rates = (
            (defect_rate < 0)
            | (defect_rate > 100)
        ).sum()

        if invalid_rates > 0:
            errors.append(
                f"{invalid_rates} row(s) have defect rates outside 0-100%."
            )

    return errors


# ============================================================
# SUPABASE UPLOAD
# ============================================================

def dataframe_to_records(df):
    """
    Convert DataFrame to JSON-safe dictionaries.
    """

    clean_df = df.copy()

    # Convert pandas timestamps into strings.
    for column in clean_df.columns:

        if pd.api.types.is_datetime64_any_dtype(
            clean_df[column]
        ):
            clean_df[column] = (
                clean_df[column]
                .dt.strftime(
                    "%Y-%m-%dT%H:%M:%S"
                )
            )

    # Replace NaN/NaT with None.
    clean_df = clean_df.where(
        pd.notnull(clean_df),
        None,
    )

    return clean_df.to_dict(
        orient="records"
    )


def upload_records(
    table_name,
    records,
    batch_size=500,
):
    """
    Upload records to Supabase in batches.
    """

    total_records = len(records)

    if total_records == 0:
        return 0

    progress = st.progress(
        0,
        text="Preparing upload...",
    )

    uploaded = 0

    for start in range(
        0,
        total_records,
        batch_size,
    ):

        batch = records[
            start:start + batch_size
        ]

        try:
            response = (
                supabase
                .table(table_name)
                .insert(batch)
                .execute()
            )

        except Exception as e:
            progress.empty()

            raise RuntimeError(
                f"Supabase upload failed: {e}"
            ) from e

        if response is None:
            progress.empty()

            raise RuntimeError(
                "Supabase returned an empty response."
            )

        uploaded += len(batch)

        percentage = min(
            uploaded / total_records,
            1.0,
        )

        progress.progress(
            percentage,
            text=(
                f"Uploading {uploaded:,} "
                f"of {total_records:,} records..."
            ),
        )

    progress.empty()

    return uploaded


# ============================================================
# UPLOAD HANDLER
# ============================================================

def process_upload(
    uploaded_file,
    upload_type,
):
    """
    Read, validate and upload one CSV file.
    """

    config = UPLOAD_CONFIG[upload_type]

    try:

        # ----------------------------------------------------
        # READ CSV
        # ----------------------------------------------------

        df = pd.read_csv(
            uploaded_file
        )

    except Exception as e:

        st.error(
            f"Unable to read {uploaded_file.name}."
        )

        st.code(
            str(e)
        )

        return

    # --------------------------------------------------------
    # PREPARE
    # --------------------------------------------------------

    try:

        df = prepare_dataframe(
            df,
            upload_type,
        )

    except Exception as e:

        st.error(
            "Unable to prepare the uploaded data."
        )

        st.code(
            str(e)
        )

        return

    # --------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------

    errors = validate_dataframe(
        df,
        upload_type,
    )

    if errors:

        st.error(
            "The uploaded file failed validation."
        )

        for error in errors:
            st.warning(error)

        st.markdown(
            '<div class="sf-preview-title">'
            "Detected columns"
            "</div>",
            unsafe_allow_html=True,
        )

        st.code(
            ", ".join(
                map(
                    str,
                    df.columns,
                )
            )
        )

        return

    # --------------------------------------------------------
    # PREVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div class="sf-preview-title">'
        "Validated data preview"
        "</div>",
        unsafe_allow_html=True,
    )

    st.dataframe(
        df.head(10),
        width="stretch",
        hide_index=True,
    )

    # --------------------------------------------------------
    # CONFIRM UPLOAD
    # --------------------------------------------------------

    confirm_key = (
        f"confirm_{upload_type}_"
        f"{uploaded_file.name}"
    )

    upload_button = st.button(
        f"Upload {len(df):,} records",
        key=confirm_key,
        type="primary",
        width="stretch",
    )

    if not upload_button:
        return

    # --------------------------------------------------------
    # CONVERT TO RECORDS
    # --------------------------------------------------------

    records = dataframe_to_records(
        df
    )

    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

    try:

        uploaded_count = upload_records(
            config["table"],
            records,
        )

    except Exception as e:

        st.error(
            "Upload failed."
        )

        st.code(
            str(e)
        )

        return

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    upload_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    st.session_state.upload_history.insert(
        0,
        {
            "file": uploaded_file.name,
            "type": config["title"],
            "table": config["table"],
            "records": uploaded_count,
            "time": upload_time,
            "status": "Success",
        },
    )

    st.success(
        f"Successfully uploaded {uploaded_count:,} "
        f"records to `{config['table']}`."
    )

    st.cache_data.clear()

    st.rerun()


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """<div class="sf-page-header">
<h1>Upload Manufacturing Data</h1>
<p>Upload CSV files using the supported formats below. Files are validated before being added to Supabase.</p>
</div>""",
    unsafe_allow_html=True,
)


# ============================================================
# UPLOAD CARDS
# ============================================================

card_columns = st.columns(
    3,
    gap="medium",
)


# ============================================================
# MACHINE UPTIME
# ============================================================

with card_columns[0]:

    config = UPLOAD_CONFIG["uptime"]

    st.markdown(
        f"""<div class="sf-upload-card">
<div class="sf-upload-icon">{config["icon"]}</div>
<h3>{config["title"]}</h3>
<p>{config["description"]}</p>
</div>""",
        unsafe_allow_html=True,
    )

    uptime_file = st.file_uploader(
        "Machine uptime CSV",
        type=["csv"],
        key="uptime_upload",
        label_visibility="collapsed",
    )

    st.caption(
        "CSV • timestamp, machine_id, voltage, "
        "rotation_speed, pressure, vibration, is_running"
    )

    if uptime_file is not None:

        st.info(
            f"Selected: {uptime_file.name}"
        )

        process_upload(
            uptime_file,
            "uptime",
        )


# ============================================================
# MAINTENANCE
# ============================================================

with card_columns[1]:

    config = UPLOAD_CONFIG["maintenance"]

    st.markdown(
        f"""<div class="sf-upload-card">
<div class="sf-upload-icon">{config["icon"]}</div>
<h3>{config["title"]}</h3>
<p>{config["description"]}</p>
</div>""",
        unsafe_allow_html=True,
    )

    maintenance_file = st.file_uploader(
        "Maintenance records CSV",
        type=["csv"],
        key="maintenance_upload",
        label_visibility="collapsed",
    )

    st.caption(
        "CSV • timestamp, machine_id, component, "
        "log_type, next_due_date"
    )

    if maintenance_file is not None:

        st.info(
            f"Selected: {maintenance_file.name}"
        )

        process_upload(
            maintenance_file,
            "maintenance",
        )


# ============================================================
# DEFECTS
# ============================================================

with card_columns[2]:

    config = UPLOAD_CONFIG["defects"]

    st.markdown(
        f"""<div class="sf-upload-card">
<div class="sf-upload-icon">{config["icon"]}</div>
<h3>{config["title"]}</h3>
<p>{config["description"]}</p>
</div>""",
        unsafe_allow_html=True,
    )

    defect_file = st.file_uploader(
        "Defect records CSV",
        type=["csv"],
        key="defect_upload",
        label_visibility="collapsed",
    )

    st.caption(
        "CSV • timestamp, machine_id, material_name, "
        "production_output, defect_rate, defective_units, "
        "energy_consumed"
    )

    if defect_file is not None:

        st.info(
            f"Selected: {defect_file.name}"
        )

        process_upload(
            defect_file,
            "defects",
        )


# ============================================================
# DIVIDER
# ============================================================

st.divider()


# ============================================================
# UPLOAD HISTORY
# ============================================================

st.markdown(
    '<div class="sf-section-title">Upload History</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sf-section-caption">Files uploaded during this Streamlit session.</div>',
    unsafe_allow_html=True,
)


if not st.session_state.upload_history:

    st.info(
        "No uploads have been made during this session."
    )

else:

    for item in st.session_state.upload_history:

        st.markdown(
            f"""<div class="sf-history-card">
<div class="sf-history-title">{item["file"]}</div>
<div class="sf-history-meta">{item["type"]} &nbsp; • &nbsp; {item["records"]:,} records &nbsp; • &nbsp; {item["table"]} &nbsp; • &nbsp; {item["time"]}</div>
</div>""",
            unsafe_allow_html=True,
        )


# ============================================================
# SUPPORTED FORMATS
# ============================================================

with st.expander(
    "Supported CSV formats"
):

    st.markdown(
        """<div class="sf-format-box">
<h4>Machine Uptime CSV</h4>
<p>Required columns:</p>
<ul>
<li>timestamp</li>
<li>machine_id</li>
<li>voltage</li>
<li>rotation_speed</li>
<li>pressure</li>
<li>vibration</li>
<li>is_running</li>
</ul>
<h4>Maintenance Records CSV</h4>
<p>Required columns:</p>
<ul>
<li>timestamp</li>
<li>machine_id</li>
<li>component</li>
<li>log_type</li>
<li>next_due_date</li>
</ul>
<h4>Defect Records CSV</h4>
<p>Required columns:</p>
<ul>
<li>timestamp</li>
<li>machine_id</li>
<li>material_name</li>
<li>production_output</li>
<li>defect_rate</li>
<li>defective_units</li>
<li>energy_consumed</li>
</ul>
<p>CSV files are validated before they are inserted into Supabase. Machine IDs and timestamps are normalized automatically.</p>
</div>""",
        unsafe_allow_html=True,
    )