Membre du Groupe : 
- KRETZ Henri 
- MEYER Theo 
- MOLINARD Matéo 
- RAHBI Alexandre 
- VERJUS Alicia 
- ZANIN Julien

Start the API server:
```
uvicorn server.main:app --reload --host 127.0.0.1 --port 8000
```

Rajouter un fichier api_secret.py avec
"
# Token for authentification
AUTH_TOKEN = "api_token"

# Dossier où les données collectées seront sauvegardées
DATA_PATH = "server/data/historical_data/kraken_btcusdt.json"

# URLs WebSocket pour les exchanges
KRAKEN_WS_URL = "wss://ws.kraken.com"
" 

Access the Swagger documentation: [ ](http://127.0.0.1:8000/docs)

Test the endpoints:
- Submit a TWAP order via `POST /api/auth/orders/twap`.
- Check its status with `GET /api/auth/orders/{token_id}`.

Test the client with:
```
python3 client.py
```
---

## Project Structure

```
PYTHONAPI/
├── server/
│   ├── __init__.py
│   ├── main.py                 # Entry point for the server
│   ├── api/                    # REST API endpoints
│   │   ├── __init__.py
│   │   ├── public.py           # Public API endpoints (e.g., klines, exchanges)
│   │   ├── authenticated.py    # Authenticated endpoints (e.g., TWAP orders)
│   ├── core/                   # Core logic and utilities
│   │   ├── __init__.py
│   │   ├── market_data.py      # Handles market data collection and normalization
│   │   ├── twap_executor.py    # TWAP order simulation and execution logic
│   │   ├── authentication.py   # Token-based authentication logic
│   │   ├── config.py           # Configuration variables
│   ├── websocket/              # WebSocket handlers
│   │   ├── __init__.py
│   │   ├── websocket_manager.py # WebSocket management
│   ├── tests/                  # Automated tests
│       ├── __init__.py
│       ├── test_api.py         # Tests for REST API endpoints
│       ├── test_websocket.py   # Tests for WebSocket functionality
│       ├── test_twap.py        # Tests for TWAP execution logic
├── client/
│   ├── __init__.py
│   ├── client.py               # Client implementation for interacting with the server
│   ├── examples/               # Example scripts for using the client
│   │   ├── submit_order.py     # Example for submitting a TWAP order
│   │   ├── monitor_feed.py     # Example for monitoring WebSocket data
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── api_secrets                 # Environment variables (e.g., token, server URL)
```
