from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="RCaaS Reflective Auditor")

# Ensure our data directory is recognized
if not os.path.exists("data"):
    os.makedirs("data")

class AuditRequest(BaseModel):
    policy_threshold: float
    measured_value: float
    context: str

@app.get("/")
def root():
    return {"status": "RCaaS Node Online", "version": "2.0-Reflective"}

@app.post("/audit")
async def reflective_audit(request: AuditRequest):
    # Stage 1: Initial Logic
    initial_pass = request.measured_value >= request.policy_threshold
    status = "PASS" if initial_pass else "FAIL"
    
    # Stage 2: The Reflection Loop (Agentic Reasoning)
    # We simulate a 'self-correction' based on context
    final_status = status
    reflection_note = "Standard rule application."
    
    if status == "FAIL" and "buffer" in request.context.lower():
        final_status = "PASS (Conditional)"
        reflection_note = "Initial FAIL overturned: Contextual buffer identified in policy."
    
    return {
        "audit_id": "REFLECT-001",
        "reasoning": reflection_note,
        "final_result": final_status
    }