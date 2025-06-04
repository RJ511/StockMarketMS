from Models.User import User
from uuid import uuid4
from fastapi import Request # type: ignore
from fastapi.responses import RedirectResponse # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from Database.db_access import *

templates = Jinja2Templates(directory="views")

async def list_users():
    return User.all()

async def create_user(request: Request):
    form = await request.form()
    name = form["name"]
    user = User(id=str(uuid4()), name=name, balance=10000.0)
    user.save()
    return RedirectResponse(url="/users", status_code=303)

async def get_user(user_id: str):
    user = User.find(user_id)
    if not user:
        return {"error": "User not found"}
    return {
        "id": user.id,
        "name": user.name,
        "balance": user.balance
    }

async def user_edit(request: Request, user_id: str):
    user = User.find(user_id)
    return templates.TemplateResponse("user_edit.html", {"request": request, "user": user})

async def update_user(request: Request, user_id: str):
    form = await request.form()
    user = User.find(user_id)
    if user:
        user.name = form["name"]
        user.balance = float(form["balance"])
        user.update()
    return RedirectResponse(url="/users", status_code=303)

async def delete_user(user_id: str):
    user = User.find(user_id)
    if user:
        user.delete()
    return RedirectResponse(url="/users", status_code=303)



async def transfer_balance(request: Request):
    data = await request.json()
    from_id = data["from"]
    to_id = data["to"]
    amount = float(data["amount"])

    from_user = get_user_by_id(from_id)
    to_user = get_user_by_id(to_id)

    if not from_user or not to_user:
        return {"error": "Utilizador não encontrado"}

    if from_user["balance"] < amount:
        return {"error": "Saldo insuficiente"}

    update_user_balance_by_id(from_id, from_user["balance"] - amount)
    update_user_balance_by_id(to_id, to_user["balance"] + amount)

    return {"status": "Transferência efetuada com sucesso"}