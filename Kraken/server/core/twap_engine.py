from datetime import datetime, timedelta, timezone
import json
import asyncio

class TWAPEngine:
    def __init__(self, order_book_path: str):
        self.order_book_path = order_book_path
        self.executions = []

    async def read_order_book(self):
        try:
            with open(self.order_book_path, "r") as f:
                lines = f.readlines()
                if lines:
                    return json.loads(lines[-1])
        except FileNotFoundError:
            print(f"Error: File {self.order_book_path} not found.")
        return None

    async def execute_twap(self, symbol: str, quantity: float, duration: int, limit_price: float, side: str):
        slices = duration
        slice_quantity = quantity / slices
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(seconds=duration)

        while datetime.now(timezone.utc) < end_time:
            order_book = await self.read_order_book()
            if not order_book:
                await asyncio.sleep(1)
                continue
            price = None
            if side == "buy":
                price = float(order_book["asks"][0][0])
            elif side == "sell":
                price = float(order_book["bids"][0][0])

            if price is not None and ((side == "buy" and price <= limit_price) or (side == "sell" and price >= limit_price)):
                self.executions.append({"timestamp": datetime.now(timezone.utc).isoformat(), "price": price, "quantity": slice_quantity})
            await asyncio.sleep(1)

        total_executed = sum(exec["quantity"] for exec in self.executions)
        avg_price = sum(exec["price"] * exec["quantity"] for exec in self.executions) / total_executed if total_executed > 0 else 0
        return {"total_executed": total_executed, "avg_price": avg_price, "details": self.executions}
