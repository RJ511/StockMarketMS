from Models.User import User
from uuid import uuid4
from fastapi import Request  # type: ignore
from fastapi.responses import RedirectResponse  # type: ignore
from Database.db_access import *

users = {}

async def create_user(request: Request):
    form = await request.form()
    name = form["name"]
    user_id = str(uuid4())

    insert_user(user_id, name)

    return RedirectResponse(url=f"/users", status_code=303)

async def get_user(user_id: str):
    user = users.get(user_id)
    if not user:
        return {"error": "User not found"}
    return {
        "id": user.id,
        "name": user.name,
        "balance": user.balance,
        "portfolio": user.portfolio
    }

async def list_users():
    return get_all_users()