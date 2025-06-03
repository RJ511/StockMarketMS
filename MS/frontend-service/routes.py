from fastapi import APIRouter, Request  # type: ignore
from fastapi.responses import HTMLResponse  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
import httpx # type: ignore

router = APIRouter()
templates = Jinja2Templates(directory="Views")

async def fetch_html_from(service_url: str) -> HTMLResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(service_url)
    return HTMLResponse(content=response.text)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/create-user", response_class=HTMLResponse)
async def users_page(_: Request):
    return await fetch_html_from("http://localhost:1001/users-page")

@router.get("/stocks", response_class=HTMLResponse)
async def stocks_page(_: Request):
    return await fetch_html_from("http://localhost:1003/stocks-page")

@router.get("/orders", response_class=HTMLResponse)
async def orders_page(_: Request):
    return await fetch_html_from("http://localhost:1002/orders-page")
