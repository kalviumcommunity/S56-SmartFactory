-- =============================================================================
-- SmartFactory Analytics & Query Layer
-- Database: PostgreSQL / Supabase
-- Target File: sql/analytics_queries.sql
-- =============================================================================
-- Schema Tables & Columns Reference (actual Supabase columns from load_data.py):
-- 1. machines (machine_id, model, age_years, status)
-- 2. uptime_logs (timestamp, machine_id, voltage, rotation_speed, pressure, vibration, is_running)
-- 3. maintenance_logs (timestamp, machine_id, component, log_type, next_due_date)
-- 4. defect_logs (timestamp, machine_id, material_name, production_output, defect_rate, defective_units, energy_consumed)
-- =============================================================================
-- NOTE: uptime_percentage is derived on-the-fly from sensor readings.
-- A reading is considered "healthy" when:
--   voltage BETWEEN 140 AND 200
--   rotation_speed BETWEEN 300 AND 500
--   pressure BETWEEN 80 AND 130
--   vibration BETWEEN 25 AND 55
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Query 1: Average Uptime by Machine
-- -----------------------------------------------------------------------------
-- Explanation:
-- Calculates the average uptime percentage for each machine by deriving a
-- health indicator from sensor readings. Results are sorted ascending by
-- uptime percentage so underperforming machines appear at the top.
-- -----------------------------------------------------------------------------
SELECT
    m.machine_id,
    m.model,
    ROUND(
        AVG(
            CASE
                WHEN u.voltage BETWEEN 140 AND 200
                 AND u.rotation_speed BETWEEN 300 AND 500
                 AND u.pressure BETWEEN 80 AND 130
                 AND u.vibration BETWEEN 25 AND 55
                THEN 100.0
                ELSE 0.0
            END
        )::numeric, 2
    ) AS average_uptime
FROM machines m
JOIN uptime_logs u ON m.machine_id = u.machine_id
GROUP BY m.machine_id, m.model
ORDER BY average_uptime ASC;


-- -----------------------------------------------------------------------------
-- Query 2: Average Uptime Overall
-- -----------------------------------------------------------------------------
-- Explanation:
-- Computes the single fleet-wide overall average uptime percentage across all
-- uptime logs recorded in the database, derived from sensor health readings.
-- -----------------------------------------------------------------------------
SELECT
    ROUND(
        AVG(
            CASE
                WHEN voltage BETWEEN 140 AND 200
                 AND rotation_speed BETWEEN 300 AND 500
                 AND pressure BETWEEN 80 AND 130
                 AND vibration BETWEEN 25 AND 55
                THEN 100.0
                ELSE 0.0
            END
        )::numeric, 2
    ) AS overall_average_uptime
FROM uptime_logs;


-- -----------------------------------------------------------------------------
-- Query 3: Uptime Trend by Date
-- -----------------------------------------------------------------------------
-- Explanation:
-- Aggregates daily performance across all factory machines over time, returning
-- the daily average uptime percentage and estimated total daily downtime hours.
-- Downtime hours = (1 - uptime_fraction) * 24 * machine_count_for_that_day.
-- -----------------------------------------------------------------------------
SELECT
    (u.timestamp)::date AS log_date,
    ROUND(
        AVG(
            CASE
                WHEN u.voltage BETWEEN 140 AND 200
                 AND u.rotation_speed BETWEEN 300 AND 500
                 AND u.pressure BETWEEN 80 AND 130
                 AND u.vibration BETWEEN 25 AND 55
                THEN 100.0
                ELSE 0.0
            END
        )::numeric, 2
    ) AS average_uptime,
    ROUND(
        (SUM(
            CASE
                WHEN u.voltage BETWEEN 140 AND 200
                 AND u.rotation_speed BETWEEN 300 AND 500
                 AND u.pressure BETWEEN 80 AND 130
                 AND u.vibration BETWEEN 25 AND 55
                THEN 0.0
                ELSE 1.0
            END
        ) / NULLIF(COUNT(*), 0) * 24.0)::numeric, 2
    ) AS total_downtime_hours
FROM uptime_logs u
GROUP BY (u.timestamp)::date
ORDER BY log_date ASC;


-- -----------------------------------------------------------------------------
-- Query 4: Total Defects by Machine
-- -----------------------------------------------------------------------------
-- Explanation:
-- Aggregates total defective units produced by each machine across all defect logs.
-- Uses LEFT JOIN to ensure defect-free machines are included with 0 defects.
-- -----------------------------------------------------------------------------
SELECT
    m.machine_id,
    m.model,
    COALESCE(SUM(d.defective_units), 0) AS total_defects
FROM machines m
LEFT JOIN defect_logs d ON m.machine_id = d.machine_id
GROUP BY m.machine_id, m.model
ORDER BY total_defects DESC;


-- -----------------------------------------------------------------------------
-- Query 5: Total Defects by Defect Type (Material Name)
-- -----------------------------------------------------------------------------
-- Explanation:
-- Summarizes total defective units and total defect log incident occurrences
-- grouped by material name (defect classification).
-- -----------------------------------------------------------------------------
SELECT
    d.material_name AS defect_type,
    COUNT(*) AS total_occurrences,
    SUM(d.defective_units) AS total_defects
FROM defect_logs d
GROUP BY d.material_name
ORDER BY total_defects DESC;


-- -----------------------------------------------------------------------------
-- Query 6: Maintenance Count by Machine
-- -----------------------------------------------------------------------------
-- Explanation:
-- Counts total maintenance events per machine, broken down into Scheduled
-- maintenance and Failure maintenance using conditional aggregation.
-- -----------------------------------------------------------------------------
SELECT
    m.machine_id,
    m.model,
    COUNT(ml.timestamp) AS total_maintenance_count,
    COUNT(CASE WHEN ml.log_type = 'Scheduled' THEN 1 END) AS preventive_count,
    COUNT(CASE WHEN ml.log_type = 'Failure' THEN 1 END) AS corrective_count
FROM machines m
LEFT JOIN maintenance_logs ml ON m.machine_id = ml.machine_id
GROUP BY m.machine_id, m.model
ORDER BY total_maintenance_count DESC;


-- -----------------------------------------------------------------------------
-- Query 7: Machines with Below-Average Uptime
-- -----------------------------------------------------------------------------
-- Explanation:
-- Identifies machines whose individual average uptime percentage is strictly less
-- than the overall fleet average uptime percentage across all machines.
-- -----------------------------------------------------------------------------
WITH machine_uptime AS (
    SELECT
        m.machine_id,
        m.model,
        ROUND(
            AVG(
                CASE
                    WHEN u.voltage BETWEEN 140 AND 200
                     AND u.rotation_speed BETWEEN 300 AND 500
                     AND u.pressure BETWEEN 80 AND 130
                     AND u.vibration BETWEEN 25 AND 55
                    THEN 100.0
                    ELSE 0.0
                END
            )::numeric, 2
        ) AS average_uptime
    FROM machines m
    JOIN uptime_logs u ON m.machine_id = u.machine_id
    GROUP BY m.machine_id, m.model
),
overall_uptime AS (
    SELECT AVG(average_uptime) AS overall_avg
    FROM machine_uptime
)
SELECT
    mu.machine_id,
    mu.model,
    mu.average_uptime,
    ROUND(ou.overall_avg::numeric, 2) AS overall_average_uptime
FROM machine_uptime mu, overall_uptime ou
WHERE mu.average_uptime < ou.overall_avg
ORDER BY mu.average_uptime ASC;


-- -----------------------------------------------------------------------------
-- Query 8: Machines with Above-Average Defect Counts
-- -----------------------------------------------------------------------------
-- Explanation:
-- Identifies machines whose cumulative defect count is strictly greater than
-- the overall average defect count per machine across the fleet.
-- -----------------------------------------------------------------------------
WITH machine_defects AS (
    SELECT
        m.machine_id,
        m.model,
        COALESCE(SUM(d.defective_units), 0) AS total_defects
    FROM machines m
    LEFT JOIN defect_logs d ON m.machine_id = d.machine_id
    GROUP BY m.machine_id, m.model
),
overall_defects AS (
    SELECT AVG(total_defects) AS avg_machine_defects
    FROM machine_defects
)
SELECT
    md.machine_id,
    md.model,
    md.total_defects,
    ROUND(od.avg_machine_defects::numeric, 2) AS overall_average_defects
FROM machine_defects md, overall_defects od
WHERE md.total_defects > od.avg_machine_defects
ORDER BY md.total_defects DESC;


-- -----------------------------------------------------------------------------
-- Query 9: Rule-Based Early-Warning Indicator Query
-- -----------------------------------------------------------------------------
-- Explanation:
-- Evaluates machine risk levels using a rule-based early warning mechanism without
-- machine learning or schema changes.
-- Flags a machine with risk_level = 'HIGH' when:
--   - its average_uptime is BELOW the overall average uptime
--   AND
--   - its total_defects count is ABOVE the overall average defect count per machine.
-- Returns 'NORMAL' otherwise.
-- -----------------------------------------------------------------------------
WITH machine_metrics AS (
    SELECT
        m.machine_id,
        m.model,
        ROUND(
            AVG(
                CASE
                    WHEN u.voltage BETWEEN 140 AND 200
                     AND u.rotation_speed BETWEEN 300 AND 500
                     AND u.pressure BETWEEN 80 AND 130
                     AND u.vibration BETWEEN 25 AND 55
                    THEN 100.0
                    ELSE 0.0
                END
            )::numeric, 2
        ) AS average_uptime,
        COALESCE(SUM(d.defective_units), 0) AS total_defects
    FROM machines m
    LEFT JOIN uptime_logs u ON m.machine_id = u.machine_id
    LEFT JOIN defect_logs d ON m.machine_id = d.machine_id
    GROUP BY m.machine_id, m.model
),
fleet_benchmarks AS (
    SELECT
        AVG(average_uptime) AS overall_avg_uptime,
        AVG(total_defects) AS overall_avg_defects
    FROM machine_metrics
)
SELECT
    mm.machine_id,
    mm.model,
    mm.average_uptime,
    mm.total_defects,
    CASE
        WHEN mm.average_uptime < fb.overall_avg_uptime
         AND mm.total_defects > fb.overall_avg_defects
        THEN 'HIGH'
        ELSE 'NORMAL'
    END AS risk_level
FROM machine_metrics mm, fleet_benchmarks fb
ORDER BY
    CASE WHEN mm.average_uptime < fb.overall_avg_uptime AND mm.total_defects > fb.overall_avg_defects THEN 1 ELSE 2 END,
    mm.average_uptime ASC,
    mm.total_defects DESC;

