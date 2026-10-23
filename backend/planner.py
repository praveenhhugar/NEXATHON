import random

# The three strategies from your CONTRACT.md
STRATEGIES = ["fake_admin_portal", "fake_config_trail", "fake_cloud_page"]

def plan(assessment, stats):
    risk = assessment.get("risk", 0)
    intent = assessment.get("intent", "normal")

    # 1. Base Rule Logic
    if risk < 30:
        return {
            "action": "continue_monitoring",
            "strategy": None,
            "reason": "Risk is low. Continuing to monitor traffic.",
            "validated": True
        }
    elif risk < 45:
        return {
            "action": "raise_logging",
            "strategy": None,
            "reason": f"Suspicious activity ({intent}) detected. Raising logging levels.",
            "validated": True
        }
    
    # 2. Strategy Selection (If risk is high)
    # If we have no stats yet, just pick the one that matches the intent
    if not stats:
        if intent == "credential_harvesting":
            strategy = "fake_config_trail"
        elif intent == "admin_probing":
            strategy = "fake_admin_portal"
        else:
            strategy = "fake_cloud_page"
    else:
        # (This is where M3's database stats will be used later)
        strategy = "fake_config_trail" 

    # 3. Return the final Decision
    return {
        "action": "deploy_decoy",
        "strategy": strategy,
        "reason": f"High risk ({risk}) with intent '{intent}'. Deploying matching decoy.",
        "validated": True
    }

# Test block (runs only if you run `python planner.py`)
if __name__ == "__main__":
    test_assessment = {"risk": 85, "intent": "credential_harvesting"}
    print(plan(test_assessment, {}))