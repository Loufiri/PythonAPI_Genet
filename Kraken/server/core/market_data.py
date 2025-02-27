import websockets
import asyncio
import json
import os
from datetime import datetime, timezone

from api_secrets import BINANCE_WS_URL, DATA_PATH

def ensure_file_exists(file_path: str):
    """
    Vérifie si un fichier existe, sinon le crée.
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass

async def binance_order_book(symbol: str, output_file: str):
    """
    Collecte les données du carnet d'ordres pour une paire spécifique sur Binance.
    """
    ws_url = f"{BINANCE_WS_URL}/{symbol.lower()}@depth10@100ms"
    ensure_file_exists(output_file)  # Vérifie si le fichier existe
    async with websockets.connect(ws_url) as websocket:
        try:
            response = await websocket.recv()
            data = json.loads(response)
            # Formater les données
            formatted_data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "asks": data["asks"],
                "bids": data["bids"]
            }
            with open(output_file, "a") as f:
                f.write(json.dumps(formatted_data) + "\n")
        except Exception as e:
            print(f"Error fetching data for Binance {symbol}: {e}")
            await asyncio.sleep(1)  # Attendre avant de réessayer


async def collect_market_data():
    """
    Lance la collecte de données pour plusieurs paires et exchanges en parallèle.
    """
    tasks = [binance_order_book("btcusdt", f"{DATA_PATH}")]
    await asyncio.gather(*tasks)
