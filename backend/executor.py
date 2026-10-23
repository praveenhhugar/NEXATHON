# backend/executor.py
import logging

# The whitelist. ONLY these actions are allowed.
ALLOWED_ACTIONS = {"deploy_decoy", "ignore", "rate_limit", "alert_admin"}

# Global state. The frontend (M4) and Verifier need to know what is currently active.
ACTIVE_DECOY = None 
DECOY_STATE = {} # Maps path to strategy_id

def execute_decision(decision: dict) -> dict:
    global ACTIVE_DECOY
    
    action = decision.get("action")
    strategy = decision.get("strategy")
    
    # 1. Safety Check
    if action not in ALLOWED_ACTIONS:
        logging.warning(f"BLOCKED: Unauthorized action '{action}' requested.")
        return {"status": "rejected", "reason": "Action not in whitelist"}
    
    # 2. Execute the Action
    if action == "deploy_decoy":
        ACTIVE_DECOY = strategy
        # Map the strategy to a specific URL path for the attacker to hit
        path_map = {
            "admin_login_decoy": "/admin",
            "config_file_honeytoken": "/config",
            "cloud_dashboard_decoy": "/cloud"
        }
        DECOY_STATE[path_map.get(strategy, "/fallback")] = strategy
        logging.info(f"EXECUTED: Activated decoy '{strategy}'")
        return {"status": "success", "active_decoy": strategy}
        
    elif action == "ignore":
        return {"status": "success", "message": "Event ignored"}
        
    else:
        return {"status": "success", "message": f"Executed {action}"}