# routes.py
from fastapi import APIRouter, Request  # type: ignore
from fastapi.responses import HTMLResponse  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
from Controllers.OrderController import *

router = APIRouter()
templates = Jinja2Templates(directory="views")

@router.get("/orders-page", response_class=HTMLResponse)
async def orders_page(request: Request):
    orders = await list_orders()
    return templates.TemplateResponse("order_index.html", {
        "request": request,
        "orders": orders
    })

@router.get("/create", response_class=HTMLResponse)
async def show_create_order(request: Request):
    return await order_create_view(request)

@router.post("/orders")
async def orders_create(request: Request):
    return await create_order(request)

@router.get("/edit/{order_id}", response_class=HTMLResponse)
async def show_edit_order(request: Request, order_id: str):
    return await order_edit(request, order_id)

@router.post("/update/{order_id}")
async def orders_update(request: Request, order_id: str):
    return await update_order(request, order_id)

@router.post("/delete/{order_id}")
async def orders_delete(order_id: str):
    return await delete_order(order_id)
