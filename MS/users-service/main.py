import asyncio
from fastapi import FastAPI  # type: ignore
from fastapi.staticfiles import StaticFiles  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
from routes import router as user_router
from Database.migrate import init_db  # type: ignore
from ai_trader import run_ai_trading_loop

app = FastAPI()
app.include_router(user_router)

# app.mount("/views", StaticFiles(directory="views"), name="views")  # REMOVIDO: views são templates, não ficheiros estáticos
templates = Jinja2Templates(directory="views")




@app.on_event("startup")
async def startup_event():
    init_db()
    asyncio.create_task(run_ai_trading_loop())