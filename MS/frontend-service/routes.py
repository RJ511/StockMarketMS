from fastapi import APIRouter, Request  # type: ignore
from fastapi.responses import HTMLResponse, Response    # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
import httpx  # type: ignore


router = APIRouter()
templates = Jinja2Templates(directory="Views")

SERVICE_MAP = {
    "user": "http://users-service:8000",
    "stock": "http://stocks-service:8000",
    "order": "http://orders-service:8000",

    # Podes adicionar mais serviços aqui no futuro
}

@router.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request):
    base_url = SERVICE_MAP.get(service)
    if not base_url:
        return Response(content=f"Serviço '{service}' não encontrado", status_code=404)

    dest_url = f"{base_url}/{path}"

    async with httpx.AsyncClient() as client:
        # Cria nova request baseada na original
        proxy_req = client.build_request(
            method=request.method,
            url=dest_url,
            headers=dict(request.headers),
            content=await request.body()
        )
        proxy_res = await client.send(proxy_req, stream=True)
        content = await proxy_res.aread()

    return Response(content=content, status_code=proxy_res.status_code, headers=dict(proxy_res.headers))

async def fetch_html_from(service_url: str) -> HTMLResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(service_url)
    return HTMLResponse(content=response.text)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/users", response_class=HTMLResponse)
async def users_page(_: Request):
    return await fetch_html_from("http://users-service:8000/users-page")

@router.get("/stocks", response_class=HTMLResponse)
async def stocks_page(request: Request):
    return await fetch_html_from("http://stocks-service:8000/stocks-page")

@router.get("/orders", response_class=HTMLResponse)
async def orders_page(_: Request):
    return await fetch_html_from("http://orders-service:8000/orders-page")
