import os
import json
import pandas as pd
import requests

# 1. Parse .env file manually to avoid dependency issues
env_vars = {}
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()

supabase_url = env_vars.get("SUPABASE_URL", "").rstrip("/")
supabase_key = env_vars.get("SUPABASE_KEY", "")

if not supabase_url or not supabase_key:
    print("\n[ERROR] SUPABASE_URL or SUPABASE_KEY missing in .env file!")
    exit(1)

print(f"Connecting to Supabase REST API at: {supabase_url}")

# Configure persistent HTTP session for fast batching
session = requests.Session()
session.headers.update({
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
})

def upload_in_batches(table_name, records, batch_size=2000):
    url = f"{supabase_url}/rest/v1/{table_name}"
    total = len(records)
    print(f"\n--- Loading {total} records into '{table_name}' ---")
    
    for i in range(0, total, batch_size):
        batch = records[i:i + batch_size]
        response = session.post(url, json=batch)
        
        if response.status_code not in (200, 201, 204):
            print(f"\n[ERROR] Failed to insert into {table_name} at batch index {i}:")
            print(f"Status Code: {response.status_code}")
            print(f"Details: {response.text}")
            return False
            
        print(f"Uploaded {min(i + batch_size, total)} / {total} records...", end="\r")
    
    print(f"\n[SUCCESS] Successfully loaded all {total} records into '{table_name}'!")
    return True

# Step 1: Machines
print("\n[1/4] Processing Machines metadata...")
try:
    pdm_machines = pd.read_csv("data/raw/PdM_machines.csv")
    pdm_machines = pdm_machines.rename(columns={
        "machineID": "machine_id",
        "model": "model",
        "age": "age_years"
    })
    pdm_machines["machine_id"] = pdm_machines["machine_id"].astype(str)
    pdm_machines["status"] = "Active"

    smart_data = pd.read_csv("data/raw/smart_manufacturing_dataset.csv")
    smart_ids = smart_data["Machine ID"].unique()
    smart_machines = pd.DataFrame({
        "machine_id": smart_ids,
        "model": "unknown",
        "age_years": None,
        "status": "Active"
    })

    all_machines = pd.concat([pdm_machines, smart_machines]).drop_duplicates(subset=["machine_id"])
    machines_records = all_machines.where(pd.notnull(all_machines), None).to_dict(orient="records")
    
    upload_in_batches("machines", machines_records, batch_size=500)
except Exception as e:
    print(f"Error preparing machines: {e}")
    exit(1)

# Step 2: Maintenance Logs
print("\n[2/4] Processing Maintenance Logs...")
try:
    pdm_maint = pd.read_csv("data/raw/PdM_maint.csv")
    pdm_maint = pdm_maint.rename(columns={
        "datetime": "timestamp",
        "machineID": "machine_id",
        "comp": "component"
    })
    pdm_maint["machine_id"] = pdm_maint["machine_id"].astype(str)
    pdm_maint["log_type"] = "Scheduled"
    pdm_maint["next_due_date"] = None

    pdm_failures = pd.read_csv("data/raw/PdM_failures.csv")
    pdm_failures = pdm_failures.rename(columns={
        "datetime": "timestamp",
        "machineID": "machine_id",
        "failure": "component"
    })
    pdm_failures["machine_id"] = pdm_failures["machine_id"].astype(str)
    pdm_failures["log_type"] = "Failure"
    pdm_failures["next_due_date"] = None

    all_maint = pd.concat([pdm_maint, pdm_failures])
    maint_records = all_maint.where(pd.notnull(all_maint), None).to_dict(orient="records")
    
    upload_in_batches("maintenance_logs", maint_records, batch_size=2000)
except Exception as e:
    print(f"Error preparing maintenance logs: {e}")
    exit(1)

# Step 3: Defect Logs
print("\n[3/4] Processing Defect Logs...")
try:
    defect_df = smart_data.rename(columns={
        "Timestamp": "timestamp",
        "Machine ID": "machine_id",
        "Material Name": "material_name",
        "Production Output (Units)": "production_output",
        "Defect Rate (%)": "defect_rate",
        "Energy Consumption (kWh)": "energy_consumed"
    })
    defect_df["machine_id"] = defect_df["machine_id"].astype(str)
    defect_df["defective_units"] = (defect_df["production_output"] * defect_df["defect_rate"] / 100).round().astype(int)

    defect_df = defect_df[[
        "timestamp", "machine_id", "material_name", 
        "production_output", "defect_rate", "defective_units", "energy_consumed"
    ]]
    defect_records = defect_df.where(pd.notnull(defect_df), None).to_dict(orient="records")
    
    upload_in_batches("defect_logs", defect_records, batch_size=2000)
except Exception as e:
    print(f"Error preparing defect logs: {e}")
    exit(1)

# Step 4: Uptime Logs (Telemetry)
print("\n[4/4] Processing Telemetry / Uptime Logs...")
try:
    telemetry_df = pd.read_csv("data/raw/PdM_telemetry.csv")
    telemetry_df = telemetry_df.rename(columns={
        "datetime": "timestamp",
        "machineID": "machine_id",
        "volt": "voltage",
        "rotate": "rotation_speed",
        "pressure": "pressure",
        "vibration": "vibration"
    })
    telemetry_df["machine_id"] = telemetry_df["machine_id"].astype(str)
    telemetry_df["is_running"] = True

    telemetry_records = telemetry_df.where(pd.notnull(telemetry_df), None).to_dict(orient="records")
    
    upload_in_batches("uptime_logs", telemetry_records, batch_size=5000)
except Exception as e:
    print(f"Error preparing telemetry logs: {e}")
    exit(1)

print("\n==================================================")
print("  All data loaded successfully into Supabase! 🎉")
print("==================================================\n")
