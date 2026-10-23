# backend/decoys/admin.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/admin", response_class=HTMLResponse)
async def admin_login(request: Request):
    # Log the hit here (M1 will see this request)
    return """
    <html>
        <body style="background: #111; color: #0f0; font-family: monospace;">
            <h2>ACME CORP - ADMIN PORTAL</h2>
            <form action="/admin/login" method="post">
                <input type="text" name="user" placeholder="Username"><br><br>
                <input type="password" name="pass" placeholder="Password"><br><br>
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """