from aiohttp import ClientSession

from api_secrets import AUTH_TOKEN
from client.client import BASE_URL


async def submit_order():
    async with ClientSession() as session:
        response = await session.post(
            f"{BASE_URL}/api/auth/orders/twap",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            json={"symbol": "BTCUSDT", "quantity": 1, "duration": 60}
        )
        print(await response.json())
