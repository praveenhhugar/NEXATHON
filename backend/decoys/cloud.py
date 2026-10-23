from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/cloud", response_class=HTMLResponse)
async def cloud_dashboard():
    return "<html><body><h1>AWS Management Console (Mock)</h1><p style='color:red;'>Warning: Honeytoken account.</p></body></html>"