# SmartFactory — Intelligent Manufacturing Analytics Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://s56-smartfactory.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-Supabase%20%2F%20PostgreSQL-3ECF8E.svg)](https://supabase.com/)
[![Status](https://img.shields.io/badge/Sprint%201-Completed%20%26%20Deployed-success.svg)]()

> **Live Deployment:** [https://s56-smartfactory.streamlit.app/](https://s56-smartfactory.streamlit.app/)

---

## 🏭 Overview

**SmartFactory** is a unified industrial analytics platform that helps manufacturing companies detect early signs of equipment failure and production quality degradation. By correlating machine telemetry sensor readings, maintenance service histories, and defect logs into a single real-time dashboard, operations teams can transition from reactive repairs to predictive maintenance.

---

## ❓ Problem Statement

In typical manufacturing facilities:
- Machine sensor streams, maintenance records, and product defect logs are stored in separate, disconnected silos.
- Plant managers cannot easily determine whether high defect rates are linked to machine wear, voltage fluctuations, or delayed maintenance.
- Equipment failures cause costly unplanned downtime and scrap material waste.

---

## 🎯 Objectives & Key Solutions

- **Unified Data Pipeline**: Consolidate disparate manufacturing datasets into a normalized Supabase PostgreSQL database.
- **Root Cause Analysis**: Correlate machine health and telemetry anomalies with quality defect rates.
- **Predictive Maintenance Signals**: Flag deteriorating equipment before catastrophic failure occurs.
- **Interactive Multi-Page Dashboard**: Provide plant operators with accessible visual KPIs, filters, and exportable reports.

---

## 🚀 Key Features & Modules

| Module | Description |
| :--- | :--- |
| **📊 Operational Dashboard** | High-level overview of factory floor KPIs, overall availability, active machinery status, defect distribution, and maintenance load. |
| **⚙️ Machines Intelligence** | Machine-specific health profiles, operational status, sensor telemetry history, and age metrics. |
| **🛠️ Maintenance Logs** | Tracking of preventive scheduled maintenance vs. corrective emergency repairs with component-level breakdown. |
| **⚠️ Defect Analytics** | Production quality tracking, defect rate trends, defective unit counts, and material correlation. |
| **📑 Comprehensive Reports** | Cross-domain analytics, early warning equipment attention lists, and filtered data table downloads. |
| **📤 Data Upload & Validation** | Built-in CSV validator and upload portal that automatically normalizes and inserts records into Supabase. |
| **🎨 Settings & Preferences** | Light and Dark mode toggle, configurable risk threshold sliders, and real-time Supabase connection diagnostics. |

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: Streamlit (Multi-page architecture with custom responsive CSS design tokens)
- **Data Manipulation & Analytics**: Pandas, NumPy
- **Interactive Visualizations**: Plotly Express, Plotly Graph Objects, Streamlit Native Charts
- **Database & Cloud Storage**: Supabase (PostgreSQL), PostgREST REST API
- **Environment Management**: Python `dotenv`, Streamlit Secrets (`secrets.toml`)
- **Version Control**: Git & GitHub

---

## 🗄️ Database Schema

The database is hosted on Supabase (PostgreSQL) and comprises four core relational tables:

```
┌─────────────────┐       ┌────────────────────────┐
│    machines     │       │      uptime_logs       │
├─────────────────┤       ├────────────────────────┤
│ machine_id (PK) │◄──┐   │ timestamp (PK)         │
│ model           │   │   │ machine_id (FK)        │
│ age_years       │   ├───┤ voltage, rotation_spd  │
│ status          │   │   │ pressure, vibration    │
└─────────────────┘   │   │ is_running             │
                      │   └────────────────────────┘
                      │
                      │   ┌────────────────────────┐
                      │   │    maintenance_logs    │
                      │   ├────────────────────────┤
                      ├───┤ timestamp (PK)         │
                      │   │ machine_id (FK)        │
                      │   │ component, log_type    │
                      │   │ next_due_date          │
                      │   └────────────────────────┘
                      │
                      │   ┌────────────────────────┐
                      │   │      defect_logs       │
                      │   ├────────────────────────┤
                      └───┤ timestamp (PK)         │
                          │ machine_id (FK)        │
                          │ material_name          │
                          │ production_output      │
                          │ defect_rate, defects   │
                          │ energy_consumed        │
                          └────────────────────────┘
```

---

## 📁 Project Structure

```bash
S56-SmartFactory/
├── .streamlit/
│   ├── config.toml              # Streamlit theme and client configuration
│   └── secrets.toml             # Local Supabase credentials (gitignored)
├── assets/                      # UI icons and static assets
├── components/
│   ├── charts.py                # Reusable Plotly chart helper components
│   ├── theme.py                 # Design system, CSS tokens, and sidebar navigation
│   └── ui.py                    # Shared UI helpers and badges
├── data/
│   ├── raw/                     # Original CSV datasets
│   └── processed/               # Standardized and cleaned datasets
├── docs/                        # PRD, project specifications, and architecture notes
├── pages/
│   ├── defects.py               # Defect records & quality analytics page
│   ├── machines.py              # Equipment telemetry & machine status page
│   ├── maintenance.py           # Scheduled & corrective maintenance logs page
│   ├── reports.py               # High-level operational reports & attention list
│   ├── settings.py              # Application settings, theme mode, & thresholds
│   └── upload_data.py           # CSV data validation and Supabase upload page
├── sql/
│   └── analytics_queries.sql    # Analytical SQL queries and reporting scripts
├── app.py                       # Main application entry point & central dashboard
├── data_cleaning.py             # Data preprocessing and standardization pipeline
├── load_data.py                 # Supabase automated batch seeding script
├── readme.md                    # Project documentation
└── requirements.txt             # Python project dependencies
```

---

## 💻 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/pranjal-2507/S56-SmartFactory.git
cd S56-SmartFactory
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (or `.streamlit/secrets.toml`):
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-or-service-role-key
```

### 5. Seed Data to Supabase (Optional)
To load initial raw data batches into your Supabase database:
```bash
python load_data.py
```

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 👥 Team Members

- **Janhavi Hivarekar**
- **Pranjal Gosavi**
- **Sagar Raut**

---

## 🏁 Sprint 1 Deliverables Summary

- [x] Consolidate multiple industrial manufacturing datasets.
- [x] Standardize and clean schemas for machines, telemetry, maintenance, and defects.
- [x] Create Supabase PostgreSQL tables and analytical SQL query suite.
- [x] Develop interactive Streamlit analytics dashboard with theme toggle (Light / Dark).
- [x] Build data ingestion pipeline with in-app CSV validation.
- [x] Deploy live application on Streamlit Community Cloud: [https://s56-smartfactory.streamlit.app/](https://s56-smartfactory.streamlit.app/)