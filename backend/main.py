from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import observer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE = {"risk": 0, "intent": "normal", "active_decoy": None, "honeytoken_hit": False}

@app.get("/state")
def get_state():
    return STATE

@app.post("/event")
def receive_event(event: dict):
    global STATE
    
    # Extract the exact keys M1's simulator sends
    path = event.get("path", "/")
    method = event.get("method", "GET")   # M1 uses "method", not "action"
    attempts = event.get("attempts", 1)   # Read the real attempt count
    
    # Call M1's observer logic
    assessment = observer.calculate_risk(path, method, attempts)
    
    # Update the state
    STATE["risk"] = assessment["risk"]
    STATE["intent"] = assessment["intent"]
    
    # Trigger the honeytoken if they hit /env
    if "/env" in path:
        STATE["honeytoken_hit"] = True

    # This print helps you see the magic happen in your backend terminal
    print(f"🔥 Attack received: {path} | Risk: {assessment['risk']} | Intent: {assessment['intent']}")

    return {"assessment": assessment}

@app.post("/reset")
def reset_state():
    global STATE
    STATE = {"risk": 0, "intent": "normal", "active_decoy": None, "honeytoken_hit": False}
    return {"status": "reset"}