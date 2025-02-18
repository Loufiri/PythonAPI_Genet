import websockets
from api_secrets import AUTH_TOKEN
from aiohttp import ClientSession

BASE_URL    = "http://127.0.0.1:8000"

# Test authentification
async def query_secure_api():
    """Query a secure REST API endpoint."""
    async with ClientSession() as session:
        response = await session.get(
            f"{BASE_URL}/api/auth/secure-data",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        print(await response.text())

async def connect_secure_websocket():
    uri = f"ws://127.0.0.1:8000/api/auth/ws?token={AUTH_TOKEN}"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server!")
        while True:
            message = await websocket.recv()
            print(f"Message from server: {message}")

async def main():
    await query_secure_api()
    await connect_secure_websocket()