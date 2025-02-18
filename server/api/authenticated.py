import asyncio
from datetime import datetime, timezone
import uuid
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from http.client import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api_secrets import AUTH_TOKEN, DATA_PATH

from server.core.TWAPOrder import TWAPOrder
from server.core.market_data import collect_market_data
from server.websocket.websocket_manager import WebSocketManager

router = APIRouter()
security = HTTPBearer()
manager = WebSocketManager()
# Order storage
orders_db = {}

@router.get("/secure-data")
async def secure_endpoint(token: HTTPAuthorizationCredentials = Depends(security)):
    if token.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Access granted, Starting the data collection", "data": "This is secure information"}


@router.post("/orders/twap", summary="Submit a TWAP order")
async def create_twap_order(order: TWAPOrder):
    """
    Submits a new TWAP order and simulates its execution.
    """
    token_id = str(uuid.uuid4())
    orders_db[token_id] = {"status": "pending", "result": None}

    async def execute_order():
        try:
            # Simulated order execution
            result = {
                "total_executed": order.quantity,
                "avg_price": order.limit_price,
                "details": [
                    {"timestamp": datetime.now(timezone.utc).isoformat(), "price": order.limit_price, "quantity": order.quantity}
                ]
            }
            await asyncio.sleep(order.duration)  # Simulate execution duration
            orders_db[token_id]["status"] = "completed"
            orders_db[token_id]["result"] = result
        except Exception as e:
            orders_db[token_id]["status"] = "failed"
            orders_db[token_id]["result"] = {"error": str(e)}

    asyncio.create_task(execute_order())
    return {"token_id": token_id, "status": "submitted"}


@router.get("/orders", summary="List all orders")
async def list_orders():
    """
    Returns all submitted TWAP orders.
    """
    return orders_db


@router.get("/orders/{token_id}", summary="Get order status")
async def get_order_status(token_id: str):
    """
    Returns the status and details of a specific TWAP order.
    """
    if token_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found.")
    return orders_db[token_id]

# Websocket Handler
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket to send real-time order book data.
    """
    token = websocket.query_params.get("token")
    await manager.connect(websocket, token)
    print("Client connected!")

    while True:
        try:
            # Start collecting market data
            await collect_market_data()
            with open(DATA_PATH, 'r') as file:
                lines = file.readlines()
                if len(lines) < 1:
                    message = '\n'.join(lines)
                else:
                    message = '\n'.join(lines[-1:])
                # Send to all WebSocket clients
                await manager.send_to_all(message)
            await asyncio.sleep(5)
        except WebSocketDisconnect:
            manager.disconnect(websocket)