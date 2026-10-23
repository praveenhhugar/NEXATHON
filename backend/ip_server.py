from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Company IP Database")

# --- THE COMPANY DATABASE ---
# These are the only IPs allowed in the company network
EMPLOYEE_IPS = {
    "10.0.0.45": {"name": "Alice", "role": "Admin"},
    "10.0.0.46": {"name": "Bob", "role": "User"}
}

# Keeps track of how many times an IP hits us
IP_TRACKER = {}
BLOCKED_IPS = []

class IPCheck(BaseModel):
    ip: str

@app.post("/verify")
def verify_ip(data: IPCheck):
    ip = data.ip
    
    # 1. Check if already blocked
    if ip in BLOCKED_IPS:
        return {"status": "BLOCKED", "reason": "IP is on the blacklist"}

    # 2. Track attempts (Auto-ban after 5 hits)
    IP_TRACKER[ip] = IP_TRACKER.get(ip, 0) + 1
    if IP_TRACKER[ip] >= 5:
        BLOCKED_IPS.append(ip)
        return {"status": "BLOCKED", "reason": "Auto-banned after 5 attempts"}

    # 3. Check if it's an employee
    if ip not in EMPLOYEE_IPS:
        return {"status": "BLOCKED", "reason": "Unknown IP (Not in company database)"}

    # 4. If it's an employee, let them through
    return {"status": "ALLOWED", "reason": f"Authorized Employee: {EMPLOYEE_IPS[ip]['name']}"}