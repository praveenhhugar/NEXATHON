def calculate_risk(path: str, method: str, attempts: int) -> dict:
    if "/env" in path:
        base, intent, mitre = 40, "credential_harvesting", "T1552"
    elif "/admin" in path:
        base, intent, mitre = 55, "admin_probing", "T1595"
    elif "/config" in path:
        base, intent, mitre = 70, "credential_harvesting", "T1552"
    else:
        base, intent, mitre = 10, "normal", "T1595"

    risk = min(base + attempts * 5, 100)
    
    return {"risk": risk, "intent": intent, "mitre": mitre}

if __name__ == "__main__":
    print(calculate_risk("/env", "GET", 3))
    print(calculate_risk("/admin", "GET", 2))