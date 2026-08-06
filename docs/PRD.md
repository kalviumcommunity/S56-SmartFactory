# PRODUCT REQUIREMENT DOCUMENT (PRD)

## SmartFactory – Manufacturing Quality Early Warning System | Sprint 1

### Project Title:
SmartFactory – Manufacturing Quality Early Warning & Analytics Dashboard

### Team Members:
- Janhavi Hivarekar
- Pranjal Gosavi
- Sagar Raut

### Repository:
S56-SmartFactory

### Date & Version:
August 2026 | Version 1.0

### Mentor Review Status:


---

# 1. Problem Statement & Context

A manufacturing company logs machine uptime, maintenance reports, and defect records separately, preventing operations teams from identifying early signals that precede production quality failures.

Currently, machine performance, maintenance activity, and product quality information are stored and analyzed independently. Because these datasets are disconnected, operations teams cannot easily determine whether frequent maintenance, reduced machine uptime, or repeated machine issues are associated with higher defect rates.

This creates a reactive workflow where production quality problems are often investigated only after defects have already occurred.

### Core Business Impact

SmartFactory aims to combine machine uptime, maintenance, and defect information into a unified analytics system so that operations teams can identify machines showing potential warning signs and make better maintenance and production decisions.


---

# 2. Proposed Solution Overview

We propose building **SmartFactory**, a simple Python-based manufacturing analytics system with an interactive Streamlit dashboard.

The system will ingest manufacturing datasets, clean and standardize the data using Pandas, store processed information in a Supabase PostgreSQL database, calculate useful manufacturing KPIs, and display the results through an interactive dashboard.

### Key Core Capabilities

**Multi-Source Data Ingestion:**  
Load machine uptime, maintenance, and defect datasets into the system.

**Data Cleaning & Standardization:**  
Handle missing values, duplicate records, inconsistent machine IDs, dates, and data types using Python and Pandas.

**Data Integration:**  
Connect the datasets using common fields such as Machine ID and date/time.

**Supabase Data Storage:**  
Store cleaned manufacturing data in a centralized Supabase PostgreSQL database.

**Manufacturing Analytics:**  
Calculate useful metrics related to machine uptime, defects, and maintenance activity.

**Machine Performance Analysis:**  
Compare machine uptime, maintenance activity, and defect records to identify machines that may require attention.

**Interactive Dashboard:**  
Provide a Streamlit dashboard containing KPI cards, machine-level analysis, charts, tables, and filters.

**Machine Health / Risk Indicator:**  
Provide a simple indicator based on machine uptime, maintenance frequency, and defect history to highlight machines that may require investigation.


---

# 3. Technical Architecture & Tech Stack

| Layer / Domain | Technologies & Libraries | Purpose & Business Justification |
|---|---|---|
| Data Ingestion & Processing | Python, Pandas | Load, inspect, clean, standardize, and transform manufacturing datasets |
| Database & Backend | Supabase (PostgreSQL) | Store cleaned manufacturing data and provide centralized access for the dashboard |
| Data Analytics | Python, Pandas, PostgreSQL Queries | Calculate manufacturing KPIs and machine-level performance metrics |
| Interactive Visualization | Streamlit, Plotly | Build dashboard pages, KPI cards, interactive charts, tables, and filters |
| UI Design | Figma | Design dashboard mockups before implementation |
| Version Control | Git, GitHub | Manage collaborative development through branches and Pull Requests |
| Project Management | GitHub Projects | Track tasks through Todo, In Progress, and Done |
| Environment | Python, requirements.txt | Maintain project dependencies and reproducible development setup |


---

# 4. End-to-End Workflow Architecture

The SmartFactory system follows a six-stage data flow designed to transform separate manufacturing datasets into useful operational insights.

## Stage 1: Data Collection & Ingestion

Machine uptime, maintenance, and defect datasets are collected and loaded into Python using Pandas.

Initial data inspection includes:

- Available columns
- Number of records
- Missing values
- Duplicate records
- Data types
- Machine identifiers
- Date/time fields


## Stage 2: Data Cleaning & Standardization

The datasets are cleaned and standardized before analysis.

Cleaning includes:

- Removing duplicate records
- Handling missing values
- Standardizing Machine IDs
- Standardizing column names
- Converting date/time columns
- Correcting data types
- Checking invalid or inconsistent values


## Stage 3: Data Integration

The cleaned datasets are connected using common fields, primarily:

- Machine ID
- Date / Timestamp

This creates a consistent relationship between machine performance, maintenance activity, and production quality information.


## Stage 4: Supabase Data Storage

Processed manufacturing data is stored in a Supabase PostgreSQL database.

The database will contain tables representing:

- Machines
- Uptime
- Maintenance
- Defects

Supabase acts as the centralized data layer between the processed manufacturing data and the Streamlit application.


## Stage 5: Data Analytics & KPI Calculation

Data stored in Supabase is queried and processed to calculate the main dashboard metrics.

These include:

- Total Machines
- Average Uptime
- Total Defects
- Maintenance Due
- Defects by Machine
- Uptime Trends
- Recent Maintenance Activity
- Machine-level Performance
- Machine Health / Risk Indicator


## Stage 6: Streamlit Dashboard

The processed information is displayed through an interactive Streamlit application.

The dashboard includes:

- KPI cards
- Machine uptime trends
- Defects by machine
- Recent maintenance records
- Machine-level details
- Filters
- Machine health/risk indicators


---

# 5. System Architecture

The high-level system flow is:

Manufacturing Data Sources  
↓  
Machine Uptime + Maintenance Records + Defect Records  
↓  
Python + Pandas  
↓  
Data Cleaning & Processing  
↓  
Supabase (PostgreSQL)  
↓  
Data Queries & KPI Calculations  
↓  
Streamlit + Plotly Dashboard  
↓  
Factory Manager / Maintenance Engineer / Operations Team


---

# 6. Target Users

## Factory Manager

The Factory Manager uses the dashboard to monitor overall machine performance, production quality, and important manufacturing KPIs.

## Maintenance Engineer

The Maintenance Engineer uses maintenance history, uptime information, and machine health indicators to identify machines that may require attention.

## Operations Team

The Operations Team uses uptime, maintenance, and defect trends to investigate production problems and make operational decisions.


---

# 7. Functional Requirements

The SmartFactory application should allow users to:

1. Load manufacturing datasets.
2. Clean and preprocess manufacturing data.
3. Store processed data in Supabase.
4. Retrieve manufacturing data from Supabase.
5. View overall manufacturing KPIs.
6. View machine uptime trends.
7. Compare defects across machines.
8. View recent maintenance activity.
9. Filter information by machine and date where applicable.
10. View details for individual machines.
11. Identify machines showing poor performance or increased quality issues.
12. View a simple machine health/risk indicator.


---

# 8. Non-Functional Requirements

The SmartFactory application should:

- Be simple and easy to use.
- Have a clean and consistent interface.
- Load dashboard information within a reasonable time.
- Maintain consistent Machine IDs across datasets.
- Handle missing or incorrect data without crashing.
- Use modular and readable Python code.
- Store database credentials securely.
- Support collaborative development through GitHub.
- Be easy to run locally using documented setup instructions.


---

# 9. Key Performance Indicators & Business Metrics

| Metric Name | Calculation / Business Logic | Purpose |
|---|---|---|
| Total Machines | Count of unique Machine IDs | Shows the total number of monitored machines |
| Average Uptime | Average of machine uptime percentage | Measures overall machine availability |
| Total Defects | Sum of recorded defects | Shows the overall number of production quality issues |
| Defect Rate | (Defective Units / Total Units Produced) × 100 | Measures production quality performance |
| Maintenance Frequency | Number of maintenance records per machine | Identifies machines requiring frequent maintenance |
| Maintenance Due | Count of machines requiring scheduled maintenance | Supports preventive maintenance decisions |
| Machine Health Indicator | Based on uptime, defect history, and maintenance activity | Highlights machines that may require investigation |


---

# 10. Dashboard Requirements

The SmartFactory dashboard will follow the approved Figma UI mockups.

## Main Dashboard

The main dashboard will display:

- Total Machines
- Average Uptime
- Total Defects
- Maintenance Due
- Uptime Trend
- Defects by Machine
- Recent Maintenance Activity


## Machines Page

The Machines page will provide:

- Machine list
- Machine ID
- Machine name/type where available
- Machine status
- Uptime percentage
- Defect information
- Maintenance information
- Machine details option


## Machine Details Page

The Machine Details page will provide:

- Machine information
- Machine health status
- Uptime trend
- Maintenance history
- Defect history


## Upload Data Page

The Upload Data page will provide options for manufacturing data such as:

- Machine Uptime Data
- Maintenance Records
- Defect Records

The exact upload workflow will depend on the finalized data pipeline and Supabase integration.


---

# 11. MVP Scope

The Sprint 1 MVP will include:

- Manufacturing dataset ingestion
- Data inspection
- Data cleaning and preprocessing
- Data integration
- Supabase PostgreSQL database
- Data queries and KPI calculations
- Streamlit dashboard
- KPI cards
- Uptime visualization
- Defect visualization
- Maintenance information
- Machine-level analysis
- Basic filtering
- Basic machine health/risk indicator


---

# 12. Out of Scope / Future Enhancements

The following features are not required for the initial Sprint 1 MVP:

- Real-time IoT sensor integration
- Complex machine learning models
- Automatic predictive maintenance
- SMS or email alerts
- Enterprise authentication
- Real-time factory control
- Large-scale cloud infrastructure
- Advanced AI-based failure prediction

These features may be considered as future enhancements after the MVP has been successfully completed.


---

# 13. 7-Day Iterative Development Plan

The team will work collaboratively using separate Git branches and integrate completed work through Pull Requests.

## Day 1 – Workspace & Application Setup

### Focus:
Initial implementation setup

### Key Deliverables:

- Create development branches
- Set up Streamlit project structure
- Configure requirements.txt
- Configure .gitignore
- Verify application runs locally
- Begin dataset inspection
- Organize GitHub Project board

### Target Output:
Working development environment and initial Streamlit application

### Mentor Approval:
[x] Reviewed


## Day 2 – Data Inspection & Dashboard Layout

### Focus:
Data understanding and UI implementation

### Key Deliverables:

- Inspect manufacturing datasets
- Identify important dataset columns
- Profile missing values and data types
- Begin converting Figma mockups into Streamlit
- Build main dashboard layout
- Build KPI cards
- Continue GitHub Project documentation

### Target Output:
Dataset understanding and initial dashboard UI

### Mentor Approval:
[ ] Pending Review


## Day 3 – Data Cleaning & Dashboard Visualizations

### Focus:
Clean manufacturing data and develop dashboard visualizations

### Key Deliverables:

- Handle missing values
- Remove duplicates
- Standardize Machine IDs
- Standardize dates and data types
- Save processed datasets
- Create Uptime Trend visualization
- Create Defects by Machine visualization
- Add Recent Maintenance table

### Target Output:
Cleaned datasets and functional dashboard visualizations

### Mentor Approval:
[ ] Pending Review


## Day 4 – Supabase Integration & Application Pages

### Focus:
Database integration and application development

### Key Deliverables:

- Set up Supabase project
- Create required PostgreSQL tables
- Upload processed manufacturing data
- Verify database connectivity
- Build Machines page
- Build Machine Details page
- Build Upload Data page

### Target Output:
Working Supabase database and application pages

### Mentor Approval:
[ ] Pending Review


## Day 5 – Analytics & Dashboard Integration

### Focus:
Connect Supabase data with the Streamlit dashboard

### Key Deliverables:

- Retrieve data from Supabase
- Calculate dashboard KPIs
- Calculate machine-level metrics
- Replace placeholder values with actual data
- Connect charts to Supabase data
- Connect tables to Supabase data
- Add basic dashboard filters

### Target Output:
Data-driven Streamlit dashboard connected to Supabase

### Mentor Approval:
[ ] Pending Review


## Day 6 – Testing & Refinement

### Focus:
Application testing and UI improvements

### Key Deliverables:

- Test dashboard navigation
- Test filters
- Validate KPI values
- Validate charts and tables
- Test Supabase connectivity
- Identify and fix bugs
- Improve dashboard UI
- Update documentation

### Target Output:
Stable and tested SmartFactory application

### Mentor Approval:
[ ] Pending Review


## Day 7 – Final Integration & Demo

### Focus:
Final project preparation

### Key Deliverables:

- Complete end-to-end testing
- Finalize README
- Finalize project documentation
- Review GitHub issues
- Update Kanban board
- Prepare final presentation
- Prepare application demo
- Complete final mentor review

### Target Output:
Final SmartFactory application and project presentation

### Mentor Approval:
[ ] Pending Review


---

# 14. Team Contribution Plan

## Member 1 – Janhavi Hivarekar
### UI, Streamlit & Integration

Responsibilities:

- Create Figma UI mockups
- Set up Streamlit application
- Develop main dashboard
- Develop KPI cards
- Create Plotly visualizations
- Build application pages
- Implement dashboard navigation
- Connect frontend with Supabase data
- Integrate work from other team members
- Perform final UI improvements


## Member 2 – Pranjal Gosavi
### Data Engineering & Backend

Responsibilities:

- Collect/finalize manufacturing datasets
- Inspect dataset structure
- Perform data profiling
- Clean manufacturing datasets
- Handle missing values and duplicates
- Standardize Machine IDs and dates
- Integrate related datasets
- Set up Supabase database
- Create PostgreSQL tables
- Upload processed data to Supabase
- Create data queries
- Calculate required KPIs
- Support dashboard integration


## Member 3 – Sagar Raut
### Documentation, Project Management & Testing

Responsibilities:

- Maintain GitHub Kanban board
- Create and maintain GitHub issues
- Track Todo, In Progress, and Done tasks
- Update README
- Maintain project documentation
- Document datasets
- Document system architecture
- Document database structure
- Test dashboard functionality
- Report bugs through GitHub Issues
- Prepare testing notes
- Prepare presentation content
- Assist with final demo preparation


---

# 15. Git & Collaboration Workflow

The project will use one shared GitHub repository:

S56-SmartFactory

Development will take place using separate branches.

main  
│  
├── feature/dashboard-ui – Janhavi Hivarekar  
├── feature/data-pipeline – Pranjal Gosavi  
└── docs/project-docs – Sagar Raut  

Each team member will follow this workflow:

1. Pull the latest version of main.
2. Work on their assigned branch.
3. Make small and meaningful commits.
4. Push changes to their branch.
5. Create a Pull Request.
6. Assign another team member as reviewer.
7. Resolve any conflicts or review comments.
8. Merge into main after review.

Direct implementation pushes to the main branch will be avoided.


---

# 16. Team Coordination Strategy

The three contribution lanes are designed so that team members can work in parallel.

### Janhavi Hivarekar

Can initially develop the Streamlit dashboard using placeholder data while the actual data pipeline is being developed.

### Pranjal Gosavi

Can independently inspect, clean, process, and upload manufacturing data to Supabase.

### Sagar Raut

Can independently maintain project documentation, GitHub tasks, and later test completed application features.

During the integration stage, Janhavi and Pranjal will coordinate to replace placeholder dashboard data with actual Supabase data.

Sagar will test the integrated application and report any identified issues.


---

# 17. Data Structure

The exact columns will depend on the finalized manufacturing datasets.

However, the system will primarily require information related to:

### Machine Information

- Machine ID
- Machine Name / Type
- Machine Status


### Uptime Information

- Machine ID
- Date / Timestamp
- Uptime
- Downtime


### Maintenance Information

- Machine ID
- Maintenance Date
- Maintenance Type
- Maintenance Status


### Defect Information

- Machine ID
- Date / Timestamp
- Defect Count
- Defect Type

The final database schema will be adjusted according to the actual available dataset columns.


---

# 18. Supabase Database Design

The initial Supabase database is expected to contain the following tables:

## Machines

Stores basic information about each machine.

Possible fields:

- machine_id
- machine_name
- machine_type
- machine_status


## Uptime

Stores machine performance records.

Possible fields:

- uptime_id
- machine_id
- timestamp
- uptime_percentage
- downtime


## Maintenance

Stores maintenance activity.

Possible fields:

- maintenance_id
- machine_id
- maintenance_date
- maintenance_type
- maintenance_status


## Defects

Stores production defect information.

Possible fields:

- defect_id
- machine_id
- timestamp
- defect_type
- defect_count

The final table structure will depend on the selected datasets and may be adjusted during implementation.


---

# 19. Security & Configuration

Supabase credentials and API keys will not be directly hardcoded into the application source code.

Sensitive configuration will be stored using environment variables or Streamlit secrets.

Files containing credentials will be excluded from GitHub using `.gitignore`.

Example sensitive files include:

.env

.streamlit/secrets.toml

Only required public configuration will be used by the application.


---

# 20. Success Criteria

The SmartFactory Sprint 1 MVP will be considered successful when:

- Manufacturing datasets are successfully collected and inspected.
- Data is cleaned and standardized.
- Related manufacturing data can be connected using appropriate identifiers.
- Processed data is stored successfully in Supabase.
- Streamlit can retrieve required information from Supabase.
- Core manufacturing KPIs are displayed.
- Users can view machine uptime information.
- Users can compare defects across machines.
- Users can view maintenance information.
- Machine-level details are available.
- Basic filters work correctly.
- The application runs without major errors.
- Team contributions are visible through Git commits and Pull Requests.
- GitHub Project tasks reflect actual project progress.
- Final project documentation is complete.


---

# 21. Mentor Feedback & Progress Log

This section will be updated following mentor reviews during the implementation sprint.

| Sprint Stage | Mentor Feedback / Action Items | Status |
|---|---|---|
| PRD Review | Project requirements reviewed | |
| UI Mockup Review | Figma UI reviewed |  |
| System Design Review | System design reviewed; no changes required |  |
| Day 1 | Initial application and environment setup | Pending |
| Day 2 | Dataset and dashboard UI progress | Pending |
| Day 3 | Data cleaning and visualization progress | Pending |
| Day 4 | Supabase integration and application pages | Pending |
| Day 5 | Analytics and dashboard integration | Pending |
| Day 6 | Testing and application refinement | Pending |
| Day 7 | Final application and demo | Pending |


---

# 22. Final Deliverables

The final SmartFactory project will include:

- Product Requirements Document (PRD)
- System Design
- Figma UI Mockups
- Manufacturing Datasets
- Data Cleaning & Processing Pipeline
- Supabase PostgreSQL Database
- Data Queries & Analytics
- Streamlit Dashboard
- Plotly Visualizations
- GitHub Kanban Board
- GitHub Issues
- GitHub Pull Requests
- Project README
- Testing Documentation
- Final Presentation
- Working Project Demo


---

# 23. Expected Final Outcome

SmartFactory will provide a simple and unified manufacturing analytics dashboard that brings machine uptime, maintenance, and defect information together.

Instead of analyzing these records separately, factory and operations teams will be able to view machine performance from a single application and identify patterns that may indicate production quality problems.

The Sprint 1 implementation focuses on building a practical and functional MVP rather than a complex predictive system. More advanced capabilities such as machine learning, real-time IoT monitoring, and automated predictive maintenance can be introduced in future versions.


---

### Submitted by Team Members:

Janhavi Hivarekar  
Pranjal Gosavi  
Sagar Raut

### Repository:
S56-SmartFactory

### Project Track:
Manufacturing Analytics – SmartFactory | Sprint 1
