from backend.db import update_strategy_stats

def verify_attack(payload: dict, strategy_id: int) -> dict:
    if "HT-001" in str(payload.get("body", "")):
        update_strategy_stats(strategy_id, hit=True)
        return {"honeytoken_hit": True, "status": "compromised", "message": "Honeytoken HT-001 detected!"}
    
    update_strategy_stats(strategy_id, hit=False)
    return {"honeytoken_hit": False, "status": "clean", "message": "No honeytoken detected."}