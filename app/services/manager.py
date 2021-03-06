from typing import Dict, Union

from fastapi import WebSocket

from app.serializers.notifications import Push, AckResponse


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.setdefault(client_id, websocket)

    def disconnect(self, client_id):
        self.active_connections.pop(client_id)

    async def send_personal_message(self, notification: Union[Push, AckResponse], client_id: str):
        websocket = self.active_connections.get(client_id)
        await websocket.send_json(notification.json())

    async def broadcast(self, notification: Push):
        for connection in self.active_connections.values():
            await connection.send_json(notification.json())


manager = ConnectionManager()
