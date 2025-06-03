from Models.User import User
from uuid import uuid4
from fastapi import Request  # type: ignore
from fastapi.responses import RedirectResponse  # type: ignore

users = {}

async def create_user(request: Request):
    form = await request.form()
    name = form["name"]
    user_id = str(uuid4())
    user = User(id=user_id, name=name, balance=10000.0)
    users[user_id] = user
    return RedirectResponse(url=f"/users/{user_id}", status_code=303)

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