"""
SmartFactory - Day 2: Manufacturing Data Preprocessing & Schema Alignment
=========================================================================
This script preprocesses raw manufacturing datasets and formats them to match
the finalized database & app schema:

1. machines:
   - machine_id
   - machine_name
   - machine_type

2. uptime_logs:
   - machine_id
   - log_date
   - uptime_percentage
   - downtime_hours

3. maintenance_logs:
   - maintenance_id
   - machine_id
   - maintenance_date
   - maintenance_type
   - status

4. defect_logs:
   - defect_id
   - machine_id
   - log_date
   - defect_count
   - defect_type
"""

import os
import pandas as pd
import numpy as np

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


def preprocess_machines():
    """
    Generate cleaned machines dataset matching schema:
    [machine_id, machine_name, machine_type]
    """
    print("\n" + "="*60)
    print(" 1. PROCESSING MACHINES DATASET")
    print("="*60)
    
    machines_path = os.path.join(RAW_DIR, "PdM_machines.csv")
    smart_path = os.path.join(RAW_DIR, "smart_manufacturing_dataset.csv")
    
    machine_records = []
    
    if os.path.exists(machines_path):
        raw_m = pd.read_csv(machines_path)
        for _, row in raw_m.iterrows():
            m_id = str(row["machineID"])
            model = str(row["model"])
            machine_records.append({
                "machine_id": f"MAC-{m_id.zfill(2)}" if not m_id.startswith("M") and not m_id.startswith("MAC") else m_id,
                "machine_name": f"Machine Unit {m_id} ({model})",
                "machine_type": model
            })
            
    if os.path.exists(smart_path):
        smart_df = pd.read_csv(smart_path)
        smart_ids = smart_df["Machine ID"].dropna().unique()
        for s_id in smart_ids:
            s_id_str = str(s_id)
            if not any(r["machine_id"] == s_id_str for r in machine_records):
                machine_records.append({
                    "machine_id": s_id_str,
                    "machine_name": f"Manufacturing Line {s_id_str}",
                    "machine_type": "Production Line"
                })
                
    machines_df = pd.DataFrame(machine_records).drop_duplicates(subset=["machine_id"]).reset_index(drop=True)
    
    output_path = os.path.join(PROCESSED_DIR, "cleaned_machines.csv")
    machines_df.to_csv(output_path, index=False)
    print(f"Columns: {list(machines_df.columns)}")
    print(f"[SUCCESS] Saved {len(machines_df)} machine records to {output_path}")
    return machines_df


def preprocess_uptime_logs():
    """
    Generate cleaned uptime logs matching schema:
    [machine_id, log_date, uptime_percentage, downtime_hours]
    """
    print("\n" + "="*60)
    print(" 2. PROCESSING UPTIME LOGS DATASET")
    print("="*60)
    
    telemetry_path = os.path.join(RAW_DIR, "PdM_telemetry.csv")
    if not os.path.exists(telemetry_path):
        print(f"[WARNING] Telemetry file not found at {telemetry_path}")
        return
        
    df = pd.read_csv(telemetry_path)
    
    # Convert datetime and extract date
    df["log_date"] = pd.to_datetime(df["datetime"]).dt.date
    df["machine_id"] = "MAC-" + df["machineID"].astype(str).str.zfill(2)
    
    # Calculate operational health index from sensor readings to derive uptime %
    # Normal operating ranges: volt ~ 170, rotate ~ 400, pressure ~ 100, vibration ~ 40
    df["is_healthy"] = (
        (df["volt"].between(140, 200)) &
        (df["rotate"].between(300, 500)) &
        (df["pressure"].between(80, 130)) &
        (df["vibration"].between(25, 55))
    ).astype(int)
    
    # Aggregate daily per machine to preserve log_date records for trend analysis
    daily_uptime = df.groupby(["machine_id", "log_date"]).agg(
        total_hours=("is_healthy", "count"),
        healthy_hours=("is_healthy", "sum")
    ).reset_index()
    
    daily_uptime["uptime_percentage"] = (daily_uptime["healthy_hours"] / daily_uptime["total_hours"] * 100.0).round(2)
    daily_uptime["downtime_hours"] = ((100.0 - daily_uptime["uptime_percentage"]) * 24.0 / 100.0).round(2)
    
    # Format finalized schema columns
    final_df = daily_uptime[["machine_id", "log_date", "uptime_percentage", "downtime_hours"]].copy()
    final_df["log_date"] = pd.to_datetime(final_df["log_date"])
    final_df = final_df.sort_values(by=["machine_id", "log_date"]).reset_index(drop=True)
    
    output_path = os.path.join(PROCESSED_DIR, "cleaned_uptime_logs.csv")
    final_df.to_csv(output_path, index=False)
    print(f"Columns: {list(final_df.columns)}")
    print(f"[SUCCESS] Saved {len(final_df)} uptime log records to {output_path}")
    return final_df


def preprocess_maintenance_logs():
    """
    Generate cleaned maintenance logs matching schema:
    [maintenance_id, machine_id, maintenance_date, maintenance_type, status]
    """
    print("\n" + "="*60)
    print(" 3. PROCESSING MAINTENANCE LOGS DATASET")
    print("="*60)
    
    maint_path = os.path.join(RAW_DIR, "PdM_maint.csv")
    fail_path = os.path.join(RAW_DIR, "PdM_failures.csv")
    
    dfs = []
    
    if os.path.exists(maint_path):
        maint_df = pd.read_csv(maint_path)
        maint_df = maint_df.rename(columns={"datetime": "maintenance_date", "machineID": "machine_id"})
        maint_df["machine_id"] = "MAC-" + maint_df["machine_id"].astype(str).str.zfill(2)
        maint_df["maintenance_type"] = "Preventive"
        maint_df["status"] = "Completed"
        dfs.append(maint_df)
        
    if os.path.exists(fail_path):
        fail_df = pd.read_csv(fail_path)
        fail_df = fail_df.rename(columns={"datetime": "maintenance_date", "machineID": "machine_id"})
        fail_df["machine_id"] = "MAC-" + fail_df["machine_id"].astype(str).str.zfill(2)
        fail_df["maintenance_type"] = "Corrective"
        fail_df["status"] = "Completed"
        dfs.append(fail_df)
        
    combined = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    
    combined["maintenance_date"] = pd.to_datetime(combined["maintenance_date"])
    combined = combined.sort_values(by=["machine_id", "maintenance_date"]).reset_index(drop=True)
    combined["maintenance_id"] = [f"MNT-{i+1:05d}" for i in range(len(combined))]
    
    final_df = combined[["maintenance_id", "machine_id", "maintenance_date", "maintenance_type", "status"]].copy()
    
    output_path = os.path.join(PROCESSED_DIR, "cleaned_maintenance_logs.csv")
    final_df.to_csv(output_path, index=False)
    print(f"Columns: {list(final_df.columns)}")
    print(f"[SUCCESS] Saved {len(final_df)} maintenance log records to {output_path}")
    return final_df


def preprocess_defect_logs():
    """
    Generate cleaned defect logs matching schema:
    [defect_id, machine_id, log_date, defect_count, defect_type]
    """
    print("\n" + "="*60)
    print(" 4. PROCESSING DEFECT LOGS DATASET")
    print("="*60)
    
    smart_path = os.path.join(RAW_DIR, "smart_manufacturing_dataset.csv")
    if not os.path.exists(smart_path):
        print(f"[WARNING] Defect dataset not found at {smart_path}")
        return
        
    df = pd.read_csv(smart_path)
    
    df = df.rename(columns={
        "Timestamp": "log_date",
        "Machine ID": "machine_id",
        "Material Name": "defect_type",
        "Production Output (Units)": "output",
        "Defect Rate (%)": "rate"
    })
    
    df["log_date"] = pd.to_datetime(df["log_date"])
    df["machine_id"] = df["machine_id"].astype(str)
    df["defect_count"] = (df["output"] * df["rate"] / 100.0).round().astype(int)
    
    # Filter rows where defects occurred or ensure positive defect records
    df = df.sort_values(by=["machine_id", "log_date"]).reset_index(drop=True)
    df["defect_id"] = [f"DEF-{i+1:05d}" for i in range(len(df))]
    
    final_df = df[["defect_id", "machine_id", "log_date", "defect_count", "defect_type"]].copy()
    
    output_path = os.path.join(PROCESSED_DIR, "cleaned_defect_logs.csv")
    final_df.to_csv(output_path, index=False)
    print(f"Columns: {list(final_df.columns)}")
    print(f"[SUCCESS] Saved {len(final_df)} defect log records to {output_path}")
    return final_df


if __name__ == "__main__":
    print("Running SmartFactory Data Preprocessing & Final Schema Alignment...")
    preprocess_machines()
    preprocess_uptime_logs()
    preprocess_maintenance_logs()
    preprocess_defect_logs()
    print("\n==================================================")
    print("  Preprocessing & Schema Alignment Completed! 🎉")
    print("==================================================\n")
