from fastapi import APIRouter, Request  # type: ignore
from fastapi.responses import HTMLResponse  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
from Controllers.UserController import *

router = APIRouter()
templates = Jinja2Templates(directory="views")

router.add_api_route("/create-user", create_user, methods=["POST"])
router.add_api_route("/get-user/{user_id}", get_user, methods=["GET"])

@router.get("/users-page", response_class=HTMLResponse)
async def users_page(request: Request):
    users = await list_users()
    return templates.TemplateResponse("user_index.html", {"request": request, "users": users})

@router.get("/users/create", response_class=HTMLResponse)
async def users_create_page(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request, "users": users})