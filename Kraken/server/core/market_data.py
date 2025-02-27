import websockets
import asyncio
import json
import os
from datetime import datetime, timezone

from api_secrets import KRAKEN_WS_URL, DATA_PATH

def ensure_file_exists(file_path: str):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass

async def kraken_order_book(symbol: str, output_file: str):
    ws_url = KRAKEN_WS_URL
    ensure_file_exists(output_file)
    async with websockets.connect(ws_url) as websocket:
        try:
            subscribe_message = {
                "event": "subscribe",
                "pair": [symbol],
                "subscription": {"name": "book"}
            }
            await websocket.send(json.dumps(subscribe_message))
            
            response = await websocket.recv()
            data = json.loads(response)
            if isinstance(data, list):
                formatted_data = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "asks": data[1].get("as", []),
                    "bids": data[1].get("bs", [])
                }
                with open(output_file, "a") as f:
                    f.write(json.dumps(formatted_data) + "\n")
        except Exception as e:
            print(f"Error fetching data for Kraken {symbol}: {e}")
            await asyncio.sleep(1)

async def collect_market_data():
    tasks = [kraken_order_book("BTC/USD", DATA_PATH)]
    await asyncio.gather(*tasks)
