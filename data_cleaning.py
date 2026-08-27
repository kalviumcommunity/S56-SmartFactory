# data_cleaning.py
# SmartFactory - Data Cleaning & Schema Standardization Pipeline

import os
import pandas as pd
import numpy as np

# Directory paths for raw and processed datasets
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


def clean_machine_id(val):
    """Helper to convert any machine ID into a clean, standard string format (e.g., MAC-01)."""
    if pd.isna(val):
        return None
    val_str = str(val).strip()
    if val_str.isdigit():
        return f"MAC-{int(val_str):02d}"
    if not val_str.startswith("MAC-") and val_str.startswith("M"):
        return f"MAC-{val_str[1:].zfill(2)}"
    return val_str


def preprocess_machines():
    """
    Cleans and unifies machine metadata across all source datasets.
    Output columns: machine_id, machine_name, machine_type, status
    """
    print("\n--- 1. Cleaning Machines Data ---")
    
    machines_path = os.path.join(RAW_DIR, "PdM_machines.csv")
    smart_path = os.path.join(RAW_DIR, "smart_manufacturing_dataset.csv")
    
    records = []
    
    # Process equipment records from predictive maintenance dataset
    if os.path.exists(machines_path):
        raw_m = pd.read_csv(machines_path)
        for _, row in raw_m.iterrows():
            m_id = clean_machine_id(row.get("machineID"))
            model = str(row.get("model", "Standard Unit")).strip()
            age = row.get("age")
            age_val = int(age) if pd.notna(age) else None
            
            records.append({
                "machine_id": m_id,
                "machine_name": f"Machine Unit {row.get('machineID')} ({model})",
                "machine_type": model,
                "age_years": age_val,
                "status": "Active"
            })
            
    # Also grab any machine IDs that only appear in the smart manufacturing dataset
    if os.path.exists(smart_path):
        smart_df = pd.read_csv(smart_path)
        if "Machine ID" in smart_df.columns:
            smart_ids = smart_df["Machine ID"].dropna().unique()
            for s_id in smart_ids:
                cleaned_id = str(s_id).strip()
                # Check if this machine is already added
                if not any(r["machine_id"] == cleaned_id for r in records):
                    records.append({
                        "machine_id": cleaned_id,
                        "machine_name": f"Manufacturing Line {cleaned_id}",
                        "machine_type": "Production Line",
                        "age_years": None,
                        "status": "Active"
                    })
                    
    # Build dataframe, remove any duplicate machine IDs, and fill remaining nulls
    df = pd.DataFrame(records)
    if not df.empty:
        df = df.dropna(subset=["machine_id"]).drop_duplicates(subset=["machine_id"]).reset_index(drop=True)
    
    out_file = os.path.join(PROCESSED_DIR, "cleaned_machines.csv")
    df.to_csv(out_file, index=False)
    print(f"Saved {len(df)} cleaned machine records -> {out_file}")
    return df


def preprocess_uptime_logs():
    """
    Cleans raw telemetry sensor records and calculates daily uptime/downtime per machine.
    Output columns: machine_id, log_date, uptime_percentage, downtime_hours
    """
    print("\n--- 2. Cleaning Uptime & Telemetry Data ---")
    
    telemetry_path = os.path.join(RAW_DIR, "PdM_telemetry.csv")
    if not os.path.exists(telemetry_path):
        print(f"Telemetry file not found at {telemetry_path}, skipping.")
        return None
        
    df = pd.read_csv(telemetry_path)
    
    # Parse timestamps and standardize machine IDs
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime"])
    df["log_date"] = df["datetime"].dt.date
    df["machine_id"] = df["machineID"].apply(clean_machine_id)
    
    # Drop rows where machine_id could not be resolved
    df = df.dropna(subset=["machine_id"])
    
    # Validate sensor values and identify healthy operational readings
    # Typical operating bounds: voltage (140-200), rotation speed (300-500), pressure (80-130), vibration (25-55)
    df["volt"] = pd.to_numeric(df["volt"], errors="coerce")
    df["rotate"] = pd.to_numeric(df["rotate"], errors="coerce")
    df["pressure"] = pd.to_numeric(df["pressure"], errors="coerce")
    df["vibration"] = pd.to_numeric(df["vibration"], errors="coerce")
    
    # Fill missing sensor readings with column median to prevent false downtime drops
    for col in ["volt", "rotate", "pressure", "vibration"]:
        df[col] = df[col].fillna(df[col].median())
    
    df["is_healthy"] = (
        df["volt"].between(140, 200) &
        df["rotate"].between(300, 500) &
        df["pressure"].between(80, 130) &
        df["vibration"].between(25, 55)
    ).astype(int)
    
    # Aggregate by machine and date to calculate uptime % and downtime hours
    daily = df.groupby(["machine_id", "log_date"]).agg(
        total_hours=("is_healthy", "count"),
        healthy_hours=("is_healthy", "sum")
    ).reset_index()
    
    # Calculate percentages safely (avoid zero division)
    daily["uptime_percentage"] = np.where(
        daily["total_hours"] > 0,
        (daily["healthy_hours"] / daily["total_hours"] * 100.0).round(2),
        0.0
    )
    # Clip between 0% and 100%
    daily["uptime_percentage"] = daily["uptime_percentage"].clip(0.0, 100.0)
    daily["downtime_hours"] = ((100.0 - daily["uptime_percentage"]) * 24.0 / 100.0).round(2)
    
    # Keep final columns and sort
    final_df = daily[["machine_id", "log_date", "uptime_percentage", "downtime_hours"]].copy()
    final_df["log_date"] = pd.to_datetime(final_df["log_date"])
    final_df = final_df.sort_values(by=["machine_id", "log_date"]).reset_index(drop=True)
    
    out_file = os.path.join(PROCESSED_DIR, "cleaned_uptime_logs.csv")
    final_df.to_csv(out_file, index=False)
    print(f"Saved {len(final_df)} uptime records -> {out_file}")
    return final_df


def preprocess_maintenance_logs():
    """
    Cleans and merges scheduled maintenance and failure breakdown records.
    Output columns: maintenance_id, machine_id, maintenance_date, maintenance_type, component, status
    """
    print("\n--- 3. Cleaning Maintenance & Breakdown Logs ---")
    
    maint_path = os.path.join(RAW_DIR, "PdM_maint.csv")
    fail_path = os.path.join(RAW_DIR, "PdM_failures.csv")
    
    dfs = []
    
    # Load scheduled maintenance events
    if os.path.exists(maint_path):
        maint_df = pd.read_csv(maint_path)
        maint_df = maint_df.rename(columns={"datetime": "maintenance_date", "machineID": "machine_id", "comp": "component"})
        maint_df["machine_id"] = maint_df["machine_id"].apply(clean_machine_id)
        maint_df["maintenance_type"] = "Preventive"
        maint_df["status"] = "Completed"
        dfs.append(maint_df)
        
    # Load unexpected equipment failures / corrective repairs
    if os.path.exists(fail_path):
        fail_df = pd.read_csv(fail_path)
        fail_df = fail_df.rename(columns={"datetime": "maintenance_date", "machineID": "machine_id", "failure": "component"})
        fail_df["machine_id"] = fail_df["machine_id"].apply(clean_machine_id)
        fail_df["maintenance_type"] = "Corrective"
        fail_df["status"] = "Completed"
        dfs.append(fail_df)
        
    if not dfs:
        print("No maintenance files found, skipping.")
        return None
        
    combined = pd.concat(dfs, ignore_index=True)
    
    # Clean up dates and remove rows with missing critical info
    combined["maintenance_date"] = pd.to_datetime(combined["maintenance_date"], errors="coerce")
    combined = combined.dropna(subset=["machine_id", "maintenance_date"])
    combined["component"] = combined["component"].fillna("General Inspection").astype(str).str.strip()
    
    # Sort chronologically and assign clean sequential IDs
    combined = combined.sort_values(by=["maintenance_date", "machine_id"]).reset_index(drop=True)
    combined["maintenance_id"] = [f"MNT-{i+1:05d}" for i in range(len(combined))]
    
    final_df = combined[["maintenance_id", "machine_id", "maintenance_date", "maintenance_type", "component", "status"]].copy()
    
    out_file = os.path.join(PROCESSED_DIR, "cleaned_maintenance_logs.csv")
    final_df.to_csv(out_file, index=False)
    print(f"Saved {len(final_df)} maintenance records -> {out_file}")
    return final_df


def preprocess_defect_logs():
    """
    Cleans defect records and production quality logs.
    Output columns: defect_id, machine_id, log_date, defect_count, defect_type, output, defect_rate
    """
    print("\n--- 4. Cleaning Defect & Quality Logs ---")
    
    smart_path = os.path.join(RAW_DIR, "smart_manufacturing_dataset.csv")
    if not os.path.exists(smart_path):
        print(f"Defect dataset not found at {smart_path}, skipping.")
        return None
        
    df = pd.read_csv(smart_path)
    
    # Rename columns to standard snake_case names
    df = df.rename(columns={
        "Timestamp": "log_date",
        "Machine ID": "machine_id",
        "Material Name": "defect_type",
        "Production Output (Units)": "output",
        "Defect Rate (%)": "defect_rate",
        "Energy Consumption (kWh)": "energy_consumed"
    })
    
    # Parse date and standardize machine ID
    df["log_date"] = pd.to_datetime(df["log_date"], errors="coerce")
    df = df.dropna(subset=["log_date", "machine_id"])
    df["machine_id"] = df["machine_id"].astype(str).str.strip()
    
    # Numeric sanitization - make sure output and rates are positive numbers
    df["output"] = pd.to_numeric(df["output"], errors="coerce").fillna(0).clip(lower=0)
    df["defect_rate"] = pd.to_numeric(df["defect_rate"], errors="coerce").fillna(0).clip(0.0, 100.0)
    
    # Calculate integer defective units
    df["defect_count"] = (df["output"] * df["defect_rate"] / 100.0).round().astype(int)
    
    # Fill any missing defect type with 'Unknown'
    df["defect_type"] = df["defect_type"].fillna("Standard Production").astype(str).str.strip()
    
    # Sort and assign sequential IDs
    df = df.sort_values(by=["log_date", "machine_id"]).reset_index(drop=True)
    df["defect_id"] = [f"DEF-{i+1:05d}" for i in range(len(df))]
    
    final_df = df[["defect_id", "machine_id", "log_date", "defect_count", "defect_type", "output", "defect_rate"]].copy()
    
    out_file = os.path.join(PROCESSED_DIR, "cleaned_defect_logs.csv")
    final_df.to_csv(out_file, index=False)
    print(f"Saved {len(final_df)} defect records -> {out_file}")
    return final_df


if __name__ == "__main__":
    print("==================================================")
    print("Starting SmartFactory Data Cleaning Pipeline...")
    print("==================================================")
    
    preprocess_machines()
    preprocess_uptime_logs()
    preprocess_maintenance_logs()
    preprocess_defect_logs()
    
    print("\n==================================================")
    print("All datasets cleaned and processed successfully! ✨")
    print("==================================================\n")
