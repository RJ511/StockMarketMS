import asyncio
import random
from Database.db_access import get_all_users, update_user_balance_by_id
import httpx # type: ignore

STOCK_SERVICE = "http://localhost:1003"
ORDER_SERVICE = "http://localhost:1002"

async def run_ai_trading_loop():
    while True:
        print("A executar lógica de IA...")
        users = get_all_users()

        for user in users:
            if not user.is_ai:
                continue

            # Obter ações disponíveis
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{STOCK_SERVICE}/api/stocks")
                stocks = resp.json()
                print("📈 Stocks recebidos:", stocks)

            if not stocks:
                continue

            stock = random.choice(stocks)
            price = stock["price"]
            quantity = random.randint(1, 5)

            if user.ai_type == "aggressive":
                print(f"IA {user.id} está a agir de forma agressiva")
                await execute_order(user.id, stock["id"], quantity, "buy" if random.random() < 0.5 else "sell")

            elif user.ai_type == "calculated":
                # lógica mais controlada: compra só se a variação for positiva
                history = await get_stock_history(stock["id"])
                if len(history["prices"]) >= 2 and history["prices"][-1] > history["prices"][-2]:
                    await execute_order(user.id, stock["id"], quantity, "buy")

        await asyncio.sleep(300)

async def execute_order(user_id, stock_id, quantity, order_type):
    async with httpx.AsyncClient() as client:
        print(f"📤 IA {user_id} vai {order_type} {quantity} de {stock_id}")
        await client.post(f"{ORDER_SERVICE}/orders", json={
            "user_id": user_id,
            "stock_id": stock_id,
            "quantity": quantity,
            "type": order_type
        })

async def get_stock_history(stock_id):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{STOCK_SERVICE}/api/stocks/history")
        history = resp.json().get(stock_id)
        return history or {"labels": [], "prices": []}
