# Controllers/StockController.py
from Models.Stock import Stock
from uuid import uuid4
from fastapi import Request  # type: ignore
from fastapi.responses import RedirectResponse  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore

templates = Jinja2Templates(directory="views")

async def list_stocks():
    return Stock.all()

async def create_stock(request: Request):
    form = await request.form()
    name = form["name"]
    price = float(form["price"])
    stock = Stock(id=str(uuid4()), name=name, price=price)
    stock.save()
    return RedirectResponse(url="/stocks", status_code=303)

async def stock_edit(request: Request, stock_id: str):
    stock = Stock.find(stock_id)
    return templates.TemplateResponse("stock_edit.html", {"request": request, "stock": stock})

async def update_stock(request: Request, stock_id: str):
    form = await request.form()
    name = form["name"]
    price = float(form["price"])
    stock = Stock.find(stock_id)
    if stock:
        stock.name = name
        stock.price = price
        stock.update()
    return RedirectResponse(url="/stocks", status_code=303)

async def delete_stock(stock_id: str):
    stock = Stock.find(stock_id)
    if stock:
        stock.delete()
    return RedirectResponse(url="/stocks", status_code=303)
