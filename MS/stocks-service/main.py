from fastapi import FastAPI  # type: ignore
from fastapi.templating import Jinja2Templates  # type: ignore
from Database.migrate import init_db
from Database.database import save_price_history
from routes import router as stock_router
from Models.Stock import Stock
import yfinance as yf  # type: ignore
import asyncio
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="Views")
app.include_router(stock_router)

TICKERS = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN"]

@app.on_event("startup")
async def startup_event():
    init_db()
    asyncio.create_task(initialize_stocks())
    asyncio.create_task(update_stock_prices_loop())


async def initialize_stocks():
    if not Stock.all():
        print("📦 A criar ações iniciais...")
        for ticker in TICKERS:
            try:
                stock_info = yf.Ticker(ticker)
                history = stock_info.history(period="5d")
                if not history.empty:
                    price = history["Close"].iloc[-1]
                    stock = Stock(id=ticker, name=ticker, price=price)
                    stock.save()
                    print(f"✅ {ticker} criado com preço {price:.2f}")
            except Exception as e:
                print(f"❌ Erro ao criar {ticker}: {e}")


async def update_stock_prices_loop():
    while True:
        await asyncio.sleep(300)  # 5 minutos
        print("🔁 A atualizar preços...")
        for stock in Stock.all():
            try:
                info = yf.Ticker(stock.id)
                data = info.history(period="1d")
                if not data.empty:
                    new_price = data["Close"].iloc[-1]
                    stock.price = new_price
                    stock.update()
                    save_price_history(stock.id, new_price)  # 👈 Adiciona isto
                    print(f"🟢 {stock.id} atualizado para {new_price:.2f}")
            except Exception as e:
                print(f"⚠️ Erro ao atualizar {stock.id}: {e}")
