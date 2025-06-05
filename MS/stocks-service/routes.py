# routes.py
from fastapi import APIRouter, Request  # type: ignore
from fastapi.responses import HTMLResponse  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
from Controllers.StockController import *
from Models.Stock import Stock # type: ignore

router = APIRouter()
templates = Jinja2Templates(directory="views")

@router.get("/stocks-page", response_class=HTMLResponse)
async def stocks_page(request: Request):
    stocks = await list_stocks()
    return templates.TemplateResponse("stock_index.html", {"request": request, "stocks": stocks})


@router.get("/create", response_class=HTMLResponse)
async def stocks_create_page(request: Request):
    return templates.TemplateResponse("stock_create.html", {"request": request})

@router.post("/stocks")
async def stocks_create(request: Request):
    return await create_stock(request)

@router.get("/edit/{stock_id}", response_class=HTMLResponse)
async def stocks_edit_page(request: Request, stock_id: str):
    return await stock_edit(request, stock_id)

@router.post("/update/{stock_id}")
async def stocks_update(request: Request, stock_id: str):
    return await update_stock(request, stock_id)

@router.post("/delete/{stock_id}")
async def stocks_delete(stock_id: str):
    return await delete_stock(stock_id)


@router.get("/api/stocks")
async def api_stocks():
    stocks = await list_stocks()
    return [stock.__dict__ for stock in stocks]

@router.post("/api/update-price")
async def api_update_price(request: Request):
    data = await request.json()
    stock_id = data["stock_id"]
    new_price = float(data["price"])
    Stock.update_stock_price(stock_id, new_price)
    return {"status": "Preço atualizado"}

