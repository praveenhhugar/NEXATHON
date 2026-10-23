from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import logging

router = APIRouter()

@router.get("/config", response_class=PlainTextResponse)
async def fake_config():
    logging.info("HONEYPOT VISITED: /config")
    return """
    # ACME CORP ENVIRONMENT VARIABLES
    AWS_ACCESS_KEY_ID=HT-001
    AWS_SECRET_ACCESS_KEY=fake_secret_key_abc123
    """