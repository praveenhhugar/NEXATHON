from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from notifier import send_alert
import db_real

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ==========================================
# FIREWALL & DECEPTOR STATE
# ==========================================
ALLOWED_IPS = ["127.0.0.1", "192.168.1.50", "192.168.1.99"]
BLOCKED_IPS = []
FLAGGED_IPS = set() 
HONEYTOKEN_HITS = []

@app.api_route("/gateway/{path:path}", methods=["GET", "POST"])
async def gateway(path: str, request: Request):
    # THE MAGIC: Check if the user is simulating an IP via headers
    client_ip = request.headers.get("X-Forwarded-For", request.client.host)
    
    # 1. FIREWALL CHECK
    if client_ip not in ALLOWED_IPS or client_ip in BLOCKED_IPS:
        return {"error": f"⛔ BLOCKED BY FIREWALL: IP {client_ip} is not on the allowlist."}
        
    # 2. STICKY SESSION
    if client_ip in FLAGGED_IPS:
        try:
            with open("decoy_page.html", "r") as file:
                return HTMLResponse(content=file.read(), status_code=200)
        except FileNotFoundError:
            return {"status": "200 OK", "data": "Decoy Data"}
        
    # 3. RISK ASSESSMENT
    hacker_paths = [".env", "admin", "config", "aws", "passwords"]
    risk = 90 if path in hacker_paths else 5
    
    # 4. ROUTING DECISION
    if risk >= 50:
        FLAGGED_IPS.add(client_ip)
        print(f"\n🚨 ATTACK DETECTED from {client_ip} on /{path}")
        try:
            with open("decoy_page.html", "r") as file:
                return HTMLResponse(content=file.read(), status_code=200)
        except FileNotFoundError:
            return {"status": "200 OK", "data": "Decoy Data"}
    else:
        return db_real.get_real_data(path)

# ==========================================
# APIS FOR THE DASHBOARD
# ==========================================
@app.get("/api/state")
def get_state():
    return {
        "trusted": ALLOWED_IPS,
        "blocked": BLOCKED_IPS,
        "flagged": list(FLAGGED_IPS),
        "honeytokens": HONEYTOKEN_HITS
    }

@app.post("/api/token/verify")
def verify_token(request: Request, data: dict):
    client_ip = request.headers.get("X-Forwarded-For", request.client.host)
    token = data.get("token")
    
    if token == "HT-0042-a9f3" or token == "admin123":
        HONEYTOKEN_HITS.append({"ip": client_ip, "token": token})
        
        if client_ip in ALLOWED_IPS: 
            ALLOWED_IPS.remove(client_ip)
        if client_ip not in BLOCKED_IPS: 
            BLOCKED_IPS.append(client_ip)
            
        print(f"\n🔥 HONEYTOKEN TRIGGERED by {client_ip}.")
        print(f"[*] FIREWALL UPDATED: {client_ip} removed from Allowlist and BLOCKED.")
        
        send_alert(client_ip)
        return {"status": "ENGAGEMENT CONFIRMED", "action": "FIREWALL RULE ADDED"}
    return {"status": "invalid token"}

@app.post("/api/reset")
def reset_system():
    global ALLOWED_IPS, BLOCKED_IPS, FLAGGED_IPS, HONEYTOKEN_HITS
    ALLOWED_IPS = ["127.0.0.1", "192.168.1.50", "192.168.1.99"]
    BLOCKED_IPS = []
    FLAGGED_IPS = set() 
    HONEYTOKEN_HITS = []
    print("\n🔄 SYSTEM RESET")
    return {"status": "System Reset Successful"}

@app.get("/api/test-firewall/{ip}")
def test_firewall(ip: str):
    if ip in BLOCKED_IPS or ip not in ALLOWED_IPS:
        return {"status": "⛔ CONNECTION REFUSED", "message": f"IP {ip} is blocked by firewall rules."}
    else:
        return {"status": "✅ CONNECTION ACCEPTED", "message": f"IP {ip} is on the allowlist. Traffic allowed."}