# Exemple d'utilisation
import asyncio
import json

from server.core.twap_engine import TWAPEngine


if __name__ == "__main__":
    async def main():
        engine = TWAPEngine(order_book_path="server/data/historical_data/binance_btcusdt.json")
        result = await engine.execute_twap(
            symbol="BTC/USDT",
            quantity=0.5,
            duration=10,
            limit_price=103281.5,
            side="buy"
        )
        print(json.dumps(result, indent=4))

    asyncio.run(main())