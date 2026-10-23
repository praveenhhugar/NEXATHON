# backend/decoys/config.py
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
import logging

router = APIRouter()

@router.get("/config", response_class=PlainTextResponse)
async def fake_config(request: Request):
    # This is the bait. The attacker will read this and try to use it.
    # When they use it, the Verifier catches them.
    logging.info("HONEYPOT VISITED: /config")
    return """
    # ACME CORP ENVIRONMENT VARIABLES
    DB_HOST=internal-db.acme.local
    DB_USER=admin
    DB_PASS=SuperSecretPassword123!
    
    # AWS CREDENTIALS
    AWS_ACCESS_KEY_ID=HT-001
    AWS_SECRET_ACCESS_KEY=fake_secret_key_abc123
    """