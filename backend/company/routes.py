from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
import json
import os

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home():
    return "<h1>Welcome to Acme Corp</h1>"

@router.get("/about", response_class=HTMLResponse)
async def about():
    return "<h1>About Us</h1>"

@router.get("/api/v1/products")
async def products():
    filepath = os.path.join(os.path.dirname(__file__), "data.json")
    with open(filepath, "r") as f:
        data = json.load(f)
    return JSONResponse(content=data)