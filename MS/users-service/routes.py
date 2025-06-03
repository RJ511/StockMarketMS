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

@router.get("/create", response_class=HTMLResponse)
async def users_create_page(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})



@router.get("/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_view(request: Request, user_id: str):
    return await user_edit(request, user_id)

@router.post("/update-user/{user_id}")
async def update_user_route(request: Request, user_id: str):
    return await update_user(request, user_id)

@router.post("/delete-user/{user_id}")
async def delete_user_route(user_id: str):
    return await delete_user(user_id)
