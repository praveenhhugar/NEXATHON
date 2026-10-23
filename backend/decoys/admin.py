from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/admin", response_class=HTMLResponse)
async def admin_login():
    return "<html><body><h2>ACME CORP - ADMIN PORTAL</h2><form><input name='user'><input name='pass' type='password'><button>Login</button></form></body></html>"