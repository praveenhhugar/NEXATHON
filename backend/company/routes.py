from fastapi import APIRouter
import json
import os

router = APIRouter()

# Get the absolute path to data.json
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@router.get("/")
def home():
    return {"status": "online", "message": "Welcome to Acme Corp Internal Portal"}

@router.get("/admin")
def admin_panel():
    return {"message": "Admin Login Required", "hint": "Try looking at the /company/aws route"}

@router.get("/aws")
def fake_aws_keys():
    # This is the trap. The attacker finds these keys and steals them.
    data = load_data()
    return {
        "message": "AWS Credentials Found",
        "credentials": data["internal_configs"]
    }