from Models.Stock import Stock
from fastapi import Request  # type: ignore

stocks = {}

async def create_stock(request: Request):
    data = await request.json()
    ticker = data["ticker"].upper()
    name = data["name"]
    price = data["price"]
    stock = Stock(ticker=ticker, name=name, price=price)
    stocks[ticker] = stock
    return {"ticker": stock.ticker, "name": stock.name, "price": stock.price}

async def get_stock(ticker: str):
    stock = stocks.get(ticker.upper())
    if not stock:
        return {"error": "Stock not found"}
    return {"ticker": stock.ticker, "name": stock.name, "price": stock.price}