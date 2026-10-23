import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def run_trial():
    try:
        # 1. Reset the server
        requests.post(f"{BASE_URL}/reset")
        
        # 2. Send the attack
        payload = {"path": "/env", "method": "GET", "attempts": 1}
        requests.post(f"{BASE_URL}/event", json=payload)
        
        # 3. Check the state
        response = requests.get(f"{BASE_URL}/state")
        state = response.json()
        
        # Return True if the honeytoken fired
        return state.get("honeytoken_hit") == True
        
    except Exception as e:
        print(f"❌ ERROR connecting to backend: {e}")
        print("Make sure 'uvicorn main:app --reload' is running in another terminal!")
        return False

print("🚀 Starting A/B Test (10 Trials)...")

adaptive_hits = 0
for i in range(10):
    print(f"Running trial {i+1}...", end=" ")
    if run_trial():
        print("✅ HIT!")
        adaptive_hits += 1
    else:
        print("❌ MISS")
    time.sleep(0.5)

print("\n==================================")
print(f"📊 ADAPTIVE DECOY SUCCESS: {adaptive_hits}/10")
print("📊 FIXED DECOY SUCCESS: 0/10 (Assumed baseline)")
print("==================================")