# backend/decoys/cloud.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/cloud", response_class=HTMLResponse)
async def cloud_dashboard(request: Request):
    return """
    <html>
        <body style="background: #232f3e; color: white; font-family: Arial;">
            <h1>AWS Management Console (Mock)</h1>
            <div style="border: 1px solid red; padding: 10px;">
                <p>Warning: You are using a Honeytoken account.</p>
            </div>
        </body>
    </html>
    """