# Controllers/OrderController.py
from Models.Order import Order
from Models.Transaction import Transaction
from uuid import uuid4
from fastapi import Request  # type: ignore
from fastapi.responses import RedirectResponse  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
import httpx  # type: ignore

async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:1001/api/users")
        return response.json()

async def fetch_stocks():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:1003/api/stocks")
        return response.json()

async def transfer_balance(buyer_id: str, seller_id: str, amount: float):
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:1001/api/transfer", json={
            "from": buyer_id,
            "to": seller_id,
            "amount": amount
        })

async def update_stock_price(stock_id: str, new_price: float):
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:1003/api/update-price", json={
            "stock_id": stock_id,
            "price": new_price
        })


templates = Jinja2Templates(directory="Views")

async def list_orders():
    return Order.all()

async def process_order_matching(order: Order):
    opposite_type = "buy" if order.type == "sell" else "sell"
    all_orders = Order.all()

    matches = [o for o in all_orders if o.type == opposite_type and o.stock_id == order.stock_id and (
        (order.type == "buy" and order.price >= o.price) or
        (order.type == "sell" and order.price <= o.price))]

    matches.sort(key=lambda o: o.price, reverse=(order.type == "sell"))

    for existing in matches:
        if order.quantity == 0:
            break

        trade_quantity = min(order.quantity, existing.quantity)
        price = existing.price  # o preço da ordem já existente dita o valor

        buyer_id = order.user_id if order.type == "buy" else existing.user_id
        seller_id = existing.user_id if order.type == "buy" else order.user_id

        # Registar transação
        t = Transaction(str(uuid4()), buyer_id, seller_id, order.stock_id, trade_quantity, price)
        t.save()

        # Transferência de saldo
        await transfer_balance(buyer_id, seller_id, trade_quantity * price)
        await update_stock_price(order.stock_id, price)


        # Atualizar quantidades
        order.quantity -= trade_quantity
        existing.quantity -= trade_quantity

        if existing.quantity == 0:
            existing.delete()
        else:
            existing.update()

        print(f"✔️ Match parcial de {trade_quantity} unidades entre {buyer_id} e {seller_id}")

    if order.quantity == 0:
        order.delete()
    else:
        order.update()

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
    await process_order_matching(order)
    return RedirectResponse(url="/orders", status_code=303)

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
