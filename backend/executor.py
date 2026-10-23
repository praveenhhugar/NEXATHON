import logging

ALLOWED_ACTIONS = {"deploy_decoy", "ignore", "rate_limit", "alert_admin"}
ACTIVE_DECOY = None 
DECOY_STATE = {} 

def execute_decision(decision: dict) -> dict:
    global ACTIVE_DECOY
    action = decision.get("action")
    strategy = decision.get("strategy")
    
    if action not in ALLOWED_ACTIONS:
        logging.warning(f"BLOCKED: Unauthorized action '{action}' requested.")
        return {"status": "rejected", "reason": "Action not in whitelist"}
    
    if action == "deploy_decoy":
        ACTIVE_DECOY = strategy
        path_map = {"admin_login_decoy": "/admin", "config_file_honeytoken": "/config", "cloud_dashboard_decoy": "/cloud"}
        DECOY_STATE[path_map.get(strategy, "/fallback")] = strategy
        logging.info(f"EXECUTED: Activated decoy '{strategy}'")
        return {"status": "success", "active_decoy": strategy}
    return {"status": "success", "message": f"Executed {action}"}