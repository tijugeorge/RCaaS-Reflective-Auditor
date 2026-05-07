import json
from fastapi import FastAPI

app = FastAPI()

@app.post("/audit/from-files")
async def run_file_audit():
    # 1. Ingesting the 'Source of Truth'
    with open("data/environmental_policy.json", "r") as f:
        policy = json.load(f)
    
    # 2. Ingesting the 'Evidence'
    with open("data/audit_telemetry.json", "r") as f:
        telemetry = json.load(f)

    # 3. Initial Logic
    raw_pass = telemetry["reading"] >= policy["threshold"]
    
    # 4. The Agentic Reflection Loop
    # The AI 'reads' the notes to see if a buffer applies
    final_status = "PASS" if raw_pass else "FAIL"
    reasoning = "Standard threshold check."

    if not raw_pass and "buffer" in telemetry["notes"].lower():
        final_status = "PASS (Conditional)"
        reasoning = f"Initial FAIL overturned. Found '{telemetry['notes']}' in evidence."

    return {
        "policy_id": policy["policy_id"],
        "result": final_status,
        "agent_reasoning": reasoning
    }