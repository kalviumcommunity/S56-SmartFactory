# Product Requirements Document (PRD)

## Product Name

SmartFactory

---

## Overview

SmartFactory is a simple data analytics platform that combines machine uptime logs, maintenance reports, and defect records into one dashboard. The system helps manufacturing teams identify patterns that may lead to production quality issues.

---

## Problem Statement

Manufacturing data is stored in separate files, making it difficult to identify relationships between machine performance, maintenance history, and product defects. This delays decision-making and increases production risks.

---

## Goal

Build a simple dashboard that combines multiple datasets and provides useful insights for manufacturing teams.

---

## Target Users

- Factory Manager
- Maintenance Engineer
- Operations Team

---

## Features

### Must Have

- Upload datasets
- Clean data
- Store data in SQLite
- Interactive dashboard
- Machine performance analysis
- Defect analysis

### Nice to Have

- Machine health score
- Basic risk indicator

---

## Success Criteria

- All datasets are combined successfully.
- Dashboard displays useful charts.
- Users can identify machines with higher defect rates.

---

## Tech Stack

- Python
- Pandas
- SQLite
- Streamlit
- Plotly
- GitHub