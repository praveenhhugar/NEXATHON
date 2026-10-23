# backend/verifier.py
from db import update_strategy_stats
from executor import ACTIVE_DECOY

def verify_attack(payload: dict, strategy_id: int) -> dict:
    """
    Checks if the attacker's payload contains the honeytoken.
    Payload example: {"ip": "1.2.3.4", "body": "AWS_ACCESS_KEY_ID=HT-001"}
    """
    # 1. Check for Honeytoken
    if "HT-001" in str(payload.get("body", "")):
        # The trap was successful!
        update_strategy_stats(strategy_id, hit=True)
        return {
            "honeytoken_hit": True,
            "status": "compromised",
            "message": "Honeytoken HT-001 detected in payload."
        }
    
    # 2. Check if they just visited the decoy (No honeytoken used yet)
    # We can check if the active decoy matches the path
    # (Simplified for the hackathon: if they hit the decoy path, it's a try)
    
    # 3. Normal activity (False positive/no trap triggered)
    update_strategy_stats(strategy_id, hit=False) # Recorded as a try but no hit
    return {
        "honeytoken_hit": False,
        "status": "clean",
        "message": "No honeytoken detected."
    }