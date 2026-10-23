from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import observer
from company import routes as company_routes
import time

app = FastAPI()

# 1. Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Include the company routes (The Acme Corp fake data)
app.include_router(company_routes.router, prefix="/company")

# 3. Global state
STATE = {"risk": 0, "intent": "normal", "active_decoy": None, "honeytoken_hit": False}

@app.get("/state")
def get_state():
    return STATE

@app.post("/reset")
def reset_state():
    global STATE
    STATE = {"risk": 0, "intent": "normal", "active_decoy": None, "honeytoken_hit": False}
    return {"status": "reset"}

@app.post("/event")
def receive_event(event: dict):
    global STATE
    
    # M1: Observe
    path = event.get("path", "/")
    method = event.get("method", "GET")
    attempts = event.get("attempts", 1)
    assessment = observer.calculate_risk(path, method, attempts)
    
    STATE["risk"] = assessment["risk"]
    STATE["intent"] = assessment["intent"]

    # M2: Mock Planner
    if STATE["risk"] >= 40:
        STATE["active_decoy"] = "fake_config_trail"
    else:
        STATE["active_decoy"] = None

    # M3: Mock Verifier
    if "aws" in path or "env" in path:
        STATE["honeytoken_hit"] = True

    print(f"🔥 Attack: {path} | Risk: {STATE['risk']} | Decoy: {STATE['active_decoy']} | HIT: {STATE['honeytoken_hit']}")

    return {"assessment": assessment, "state": STATE}