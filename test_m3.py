# test_m3.py
from backend.db import init_db, get_db
from backend.executor import execute_decision
from backend.verifier import verify_attack
import os

# Ensure we are in the right directory for the DB
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("--- 1. Initializing DB ---")
init_db()

print("\n--- 2. Executor: Deploying Decoy ---")
# Simulating M2's Planner output
fake_decision = {"action": "deploy_decoy", "strategy": "config_file_honeytoken"}
exec_result = execute_decision(fake_decision)
print("Executor Result:", exec_result) 

print("\n--- 3. Attacker Hits the Honeytoken ---")
# Simulating M1 catching the attacker using the key
attacker_payload = {"ip": "10.0.0.5", "body": "AWS_ACCESS_KEY_ID=HT-001"}
verdict = verify_attack(attacker_payload, strategy_id=2)
print("Verifier Verdict:", verdict)

print("\n--- 4. Checking Database ---")
conn = get_db()
strats = conn.execute("SELECT * FROM strategies").fetchall()
for s in strats:
    print(dict(s))
conn.close()