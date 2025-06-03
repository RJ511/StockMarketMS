from Models.User import User
from uuid import uuid4
from fastapi import Request  # type: ignore
from fastapi.responses import RedirectResponse  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
from Database.db_access import *

templates = Jinja2Templates(directory="views")

async def list_users():
    return get_all_users()

async def create_user(request: Request):
    form = await request.form()
    name = form["name"]
    user_id = str(uuid4())
    insert_user(user_id, name)
    return RedirectResponse(url="/users", status_code=303)

async def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}
    return {
        "id": user.id,
        "name": user.name,
        "balance": user.balance
    }

async def user_edit(request: Request, user_id: str):
    user = get_user_by_id(user_id)
    return templates.TemplateResponse("user_edit.html", {"request": request, "user": user})

async def update_user(request: Request, user_id: str):
    form = await request.form()
    name = form["name"]
    balance = float(form["balance"])
    update_user_by_id(user_id, name, balance)
    return RedirectResponse(url="/users", status_code=303)

async def delete_user(user_id: str):
    delete_user_by_id(user_id)
    return RedirectResponse(url="/users", status_code=303)
