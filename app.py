import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="SmartFactory",
    page_icon="🏭",
    layout="wide"
)


# ==================================================
# TEMPORARY DATA
# Will be replaced with Supabase data later.
# Field names follow the finalized database schema.
# ==================================================

machines = pd.DataFrame({
    "machine_id": [
        "CNC-01",
        "CNC-02",
        "WLD-01",
        "ASM-03",
        "INJ-02",
        "PRS-01",
        "CVY-04",
        "PKG-02"
    ],
    "machine_name": [
        "CNC Milling Machine",
        "CNC Lathe Unit",
        "Welding Station 1",
        "Assembly Robot 3",
        "Injection Molder 2",
        "Hydraulic Press 1",
        "Conveyor Belt 4",
        "Packaging Unit 2"
    ],
    "machine_type": [
        "CNC",
        "CNC",
        "Welding",
        "Assembly",
        "Injection",
        "Press",
        "Conveyor",
        "Packaging"
    ]
})


uptime_logs = pd.DataFrame({
    "machine_id": [
        "CNC-01", "CNC-01", "CNC-01",
        "CNC-02", "CNC-02", "CNC-02",
        "WLD-01", "WLD-01", "WLD-01",
        "ASM-03", "ASM-03", "ASM-03"
    ],

    "log_date": pd.to_datetime([
        "2026-08-01", "2026-08-05", "2026-08-10",
        "2026-08-01", "2026-08-05", "2026-08-10",
        "2026-08-01", "2026-08-05", "2026-08-10",
        "2026-08-01", "2026-08-05", "2026-08-10"
    ]),

    "uptime_percentage": [
        96.2, 97.1, 98.4,
        95.4, 96.5, 97.1,
        90.2, 89.5, 88.6,
        97.8, 98.5, 99.2
    ],

    "downtime_hours": [
        0.9, 0.7, 0.4,
        1.1, 0.9, 0.7,
        2.3, 2.5, 2.7,
        0.5, 0.4, 0.2
    ]
})


maintenance_logs = pd.DataFrame({
    "maintenance_id": [
        "MNT-0241",
        "MNT-0240",
        "MNT-0239",
        "MNT-0238",
        "MNT-0237"
    ],

    "machine_id": [
        "CNC-01",
        "WLD-01",
        "INJ-02",
        "PRS-01",
        "ASM-03"
    ],

    "maintenance_date": pd.to_datetime([
        "2026-08-14",
        "2026-08-12",
        "2026-08-10",
        "2026-08-08",
        "2026-08-06"
    ]),

    "maintenance_type": [
        "Preventive",
        "Corrective",
        "Preventive",
        "Inspection",
        "Corrective"
    ],

    "status": [
        "Completed",
        "Completed",
        "Scheduled",
        "Completed",
        "Pending"
    ]
})


defect_logs = pd.DataFrame({
    "defect_id": [
        "DEF-0512",
        "DEF-0498",
        "DEF-0481",
        "DEF-0463",
        "DEF-0440",
        "DEF-0421",
        "DEF-0405",
        "DEF-0398"
    ],

    "machine_id": [
        "CNC-01",
        "CNC-02",
        "WLD-01",
        "ASM-03",
        "INJ-02",
        "PRS-01",
        "CVY-04",
        "PKG-02"
    ],

    "log_date": pd.to_datetime([
        "2026-08-13",
        "2026-08-12",
        "2026-08-11",
        "2026-08-10",
        "2026-08-09",
        "2026-08-08",
        "2026-08-07",
        "2026-08-06"
    ]),

    "defect_count": [
        14,
        7,
        22,
        5,
        19,
        9,
        3,
        11
    ],

    "defect_type": [
        "Dimensional",
        "Surface Finish",
        "Welding",
        "Assembly",
        "Surface Finish",
        "Dimensional",
        "Alignment",
        "Packaging"
    ]
})


# ==================================================
# KPI CALCULATIONS
# ==================================================

total_machines = machines["machine_id"].nunique()

average_uptime = uptime_logs[
    "uptime_percentage"
].mean()

total_defects = defect_logs[
    "defect_count"
].sum()

maintenance_due = maintenance_logs[
    maintenance_logs["status"].isin(
        ["Pending", "Scheduled"]
    )
].shape[0]


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("⚡ SmartFactory")

    st.caption("Analytics Platform")

    st.divider()

    st.caption("NAVIGATION")

    st.write("📊 Dashboard")
    st.write("⚙️ Machines")
    st.write("🔧 Maintenance")
    st.write("⚠️ Defects")
    st.write("📈 Reports")
    st.write("⬆️ Upload Data")

    st.divider()

    st.write("👤 Admin User")
    st.caption("admin@smartfactory.io")


# ==================================================
# DASHBOARD HEADER
# ==================================================

st.title("Dashboard")

st.caption(
    "Monitor machine performance, maintenance activity "
    "and production defects."
)

st.divider()


# ==================================================
# KPI CARDS
# ==================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Machines",
        total_machines
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
        total_defects
    )

    st.caption(
        "Recorded defects"
    )


with col4:

    st.metric(
        "Maintenance Due",
        maintenance_due
    )

    st.caption(
        "Pending or scheduled"
    )


st.write("")


# ==================================================
# DASHBOARD CHARTS
# ==================================================

left_chart, right_chart = st.columns(
    [2, 1]
)


# --------------------------------------------------
# UPTIME TREND
# --------------------------------------------------

with left_chart:

    st.subheader(
        "Uptime Trend"
    )

    st.caption(
        "Machine uptime performance"
    )

    fig_uptime = px.line(
        uptime_logs,
        x="log_date",
        y="uptime_percentage",
        color="machine_id",
        markers=True
    )

    fig_uptime.update_layout(
        xaxis_title="Date",
        yaxis_title="Uptime (%)",
        legend_title="Machine",
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


# --------------------------------------------------
# DEFECTS BY MACHINE
# --------------------------------------------------

with right_chart:

    st.subheader(
        "Defects by Machine"
    )

    st.caption(
        "Total recorded defects"
    )

    defect_summary = (
        defect_logs
        .groupby(
            "machine_id",
            as_index=False
        )["defect_count"]
        .sum()
    )

    fig_defects = px.bar(
        defect_summary,
        x="machine_id",
        y="defect_count"
    )

    fig_defects.update_layout(
        xaxis_title="Machine",
        yaxis_title="Defects",
        showlegend=False,
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


# ==================================================
# RECENT MAINTENANCE
# ==================================================

st.subheader(
    "Recent Maintenance"
)

st.caption(
    "Latest service events"
)


recent_maintenance = (
    maintenance_logs
    .sort_values(
        by="maintenance_date",
        ascending=False
    )
    .head(5)
    .copy()
)


recent_maintenance[
    "maintenance_date"
] = recent_maintenance[
    "maintenance_date"
].dt.strftime(
    "%Y-%m-%d"
)


st.dataframe(
    recent_maintenance[
        [
            "maintenance_id",
            "machine_id",
            "maintenance_date",
            "maintenance_type",
            "status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)