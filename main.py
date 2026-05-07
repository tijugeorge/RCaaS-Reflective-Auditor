import json
import csv
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

@app.post("/audit/from-files")
async def run_file_audit():
    # 1. Ingest Data
    with open("data/environmental_policy.json", "r") as f:
        policy = json.load(f)
    with open("data/audit_telemetry.json", "r") as f:
        telemetry = json.load(f)

    # 2. Agentic Logic
    raw_pass = telemetry["reading"] >= policy["threshold"]
    final_status = "PASS" if raw_pass else "FAIL"
    reasoning = "Standard check"

    if not raw_pass and "buffer" in telemetry["notes"].lower():
        final_status = "PASS (Conditional)"
        reasoning = "Contextual buffer applied"

    # 3. NEW: The Logging Layer (The "Audit Trail")
    log_entry = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        policy["policy_id"],
        telemetry["reading"],
        final_status,
        reasoning
    ]

    # Append to a CSV file in the data folder
    log_file = "data/audit_history.csv"
    file_exists = False
    try:
        with open(log_file, 'r') as f: file_exists = True
    except FileNotFoundError: pass

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Policy_ID", "Reading", "Status", "Reasoning"])
        writer.writerow(log_entry)

    return {"status": "Audit Complete", "logged_to": log_file, "result": final_status}