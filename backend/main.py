from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import observer
import planner

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SIMULATED FIREWALL & STATE ---
BLOCKED_IPS = {"192.168.1.100"} # Pre-blocked known attacker
FLAGGED_IPS = set()             # IPs that bypassed firewall but got caught by AI
IP_ATTEMPTS = {}                # Tracks how many times an IP hit us
EVENT_LOG = []                  # Stores the live timeline

STATE = {
    "risk": 0, 
    "intent": "normal", 
    "active_decoy": None, 
    "honeytoken_hit": False,
    "firewall_status": "MONITORING",
    "blocked_ips": list(BLOCKED_IPS)
}

@app.get("/api/state")
def get_state():
    STATE["blocked_ips"] = list(BLOCKED_IPS) # Keep frontend updated
    return STATE

@app.get("/api/logs")
def get_logs():
    return {"logs": EVENT_LOG}

@app.post("/api/reset")
def reset_state():
    global STATE, FLAGGED_IPS, IP_ATTEMPTS, EVENT_LOG
    STATE = {"risk": 0, "intent": "normal", "active_decoy": None, "honeytoken_hit": False, "firewall_status": "MONITORING", "blocked_ips": list(BLOCKED_IPS)}
    FLAGGED_IPS.clear()
    IP_ATTEMPTS.clear()
    EVENT_LOG.clear() # Clear the timeline
    return {"status": "reset"}

# --- THE GATEWAY (Intercepts all company traffic) ---
@app.api_route("/company/{path:path}", methods=["GET", "POST"])
async def gateway(request: Request, path: str):
    global STATE, EVENT_LOG
    ip = request.client.host if request.client.host != "127.0.0.1" else request.headers.get("X-Forwarded-For", "10.0.0.45") 

    # 1. CHECK FIREWALL (Case 1)
    if ip in BLOCKED_IPS:
        STATE["firewall_status"] = f"BLOCKED ({ip})"
        EVENT_LOG.append({"type": "attacker", "text": f"⛔ Firewall Dropped Request from {ip}"})
        return {"error": "403 Forbidden - Dropped by Firewall"}

    # 2. CHECK IF ALREADY FLAGGED (Case 2 - Once flagged, always flagged)
    if ip in FLAGGED_IPS:
        STATE["firewall_status"] = f"DECEIVED ({ip})"
        return get_decoy_response(path)

    # 3. OBSERVE & PLAN
    IP_ATTEMPTS[ip] = IP_ATTEMPTS.get(ip, 0) + 1
    assessment = observer.calculate_risk(path, "GET", IP_ATTEMPTS[ip])
    STATE["risk"] = assessment["risk"]
    STATE["intent"] = assessment["intent"]

    # If risk is high, flag them and route to decoy
    if STATE["risk"] > 40:
        FLAGGED_IPS.add(ip)
        decision = planner.plan(assessment, {})
        STATE["active_decoy"] = decision.get("strategy")
        STATE["firewall_status"] = f"BYPASSED & TRAPPED ({ip})"
        
        # Add to timeline
        EVENT_LOG.append({"type": "attacker", "text": f"GET /company/{path} - Suspicious"})
        EVENT_LOG.append({"type": "observer", "text": f"Risk {STATE['risk']} | Intent {STATE['intent']}"})
        EVENT_LOG.append({"type": "planner", "text": f"Deploying {STATE['active_decoy']}"})
        
        # If they hit /env, trigger the honeytoken
        if "/env" in path:
            STATE["honeytoken_hit"] = True
            EVENT_LOG.append({"type": "verifier", "text": "🚨 HONEYTOKEN TRIGGERED!"})
            # CASE 3: TEACH THE FIREWALL
            BLOCKED_IPS.add(ip) 
            STATE["firewall_status"] = f"AI BLOCKED ({ip})"
            EVENT_LOG.append({"type": "system", "text": f"🛑 Firewall updated to block {ip}"})
            
        return get_decoy_response(path)

    # 4. LET THEM SEE REAL (FAKE) DATA
    STATE["firewall_status"] = f"ALLOWED ({ip})"
    return {"status": "success", "data": "Real Company Data (Safe)", "path": path}

def get_decoy_response(path):
    if "aws" in path:
        return {"keys": "AKIA-FAKE-123", "status": "Decoy Data"}
    return {"status": "Decoy Data", "message": "Welcome to the fake portal"}