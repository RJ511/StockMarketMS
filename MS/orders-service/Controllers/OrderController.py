from Models.Order import Order
from uuid import uuid4
from fastapi import Request  # type: ignore

orders = {}

async def create_order(request: Request):
    data = await request.json()

    user_id = data["user_id"]
    stock_ticker = data["stock_ticker"]
    quantity = data["quantity"]
    limit_price = data["limit_price"]
    order_type = data["order_type"]

    order_id = str(uuid4())
    order = Order(
        id=order_id,
        user_id=user_id,
        stock_ticker=stock_ticker.upper(),
        order_type=order_type,
        quantity=quantity,
        limit_price=limit_price
    )
    orders[order_id] = order

    return {"order_id": order.id, "status": order.status}