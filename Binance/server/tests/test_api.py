from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_get_klines():
    response = client.get("/api/public/klines/Binance/BTCUSDT?interval=1m&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 10