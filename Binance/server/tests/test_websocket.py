import asyncio
import websockets

async def test_websocket():
    """
    Teste la connexion au WebSocket et affiche les données reçues en continu.
    """
    uri = "ws://127.0.0.1:8000/ws/BTC/USDT"  # Assurez-vous que le symbole correspond à l'API
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket at {uri}")
            while True:
                # Recevoir les données en continu
                response = await websocket.recv()
                print(f"Received: {response}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
