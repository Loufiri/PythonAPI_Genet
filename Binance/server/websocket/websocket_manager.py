import asyncio
from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from api_secrets import AUTH_TOKEN

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    def validate_token(self, token: str) -> bool:
        return token == AUTH_TOKEN

    async def connect(self, websocket: WebSocket, token: str):
        if not self.validate_token(token):
            await websocket.close(code=1008)  # Policy Violation
            raise HTTPException(status_code=403, detail="Invalid token")
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_to_all(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


