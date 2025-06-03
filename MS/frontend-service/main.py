from fastapi import FastAPI  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
from fastapi.staticfiles import StaticFiles  # type: ignore
from routes import router

app = FastAPI()
app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="Views")