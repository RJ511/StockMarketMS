# Controllers/OrderController.py
from Models.Order import Order
from uuid import uuid4
from fastapi import Request  # type: ignore
from fastapi.responses import RedirectResponse  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
import httpx # type: ignore

async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:1001/api/users")
        return response.json()

async def fetch_stocks():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:1003/api/stocks")
        return response.json()

templates = Jinja2Templates(directory="views")

async def list_orders():
    return Order.all()

async def create_order(request: Request):
    form = await request.form()
    order = Order(
        id=str(uuid4()),
        user_id=form["user_id"],
        stock_id=form["stock_id"],
        type=form["type"],
        quantity=int(form["quantity"]),
        price=float(form["price"])
    )
    order.save()
    return RedirectResponse(url="/orders", status_code=303)

async def order_edit(request: Request, order_id: str):
    order = Order.find(order_id)
    return templates.TemplateResponse("order_edit.html", {"request": request, "order": order})

async def update_order(request: Request, order_id: str):
    form = await request.form()
    order = Order.find(order_id)
    if order:
        order.user_id = form["user_id"]
        order.stock_id = form["stock_id"]
        order.type = form["type"]
        order.quantity = int(form["quantity"])
        order.price = float(form["price"])
        order.update()
    return RedirectResponse(url="/orders", status_code=303)

async def delete_order(order_id: str):
    order = Order.find(order_id)
    if order:
        order.delete()
    return RedirectResponse(url="/orders", status_code=303)



async def order_create_view(request: Request):
    users = await fetch_users()
    stocks = await fetch_stocks()
    return templates.TemplateResponse("order_create.html", {
        "request": request,
        "users": users,
        "stocks": stocks
    })

async def order_edit(request: Request, order_id: str):
    order = Order.find(order_id)
    users = await fetch_users()
    stocks = await fetch_stocks()
    return templates.TemplateResponse("order_edit.html", {
        "request": request,
        "order": order,
        "users": users,
        "stocks": stocks
    })
