from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from services.manager import manager
from serializers.notifications import Notification


notifications_router = APIRouter()


@notifications_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            await websocket.receive()
    except WebSocketDisconnect:
        manager.disconnect(client_id)


@notifications_router.post("/send_push")
async def send_new_push(notification: Notification):
    response = {"status": "ok"}
    try:
        await manager.send_personal_message(notification, notification.client_id)
    except WebSocketDisconnect:
        response["status"] = "disconnected"
    return response
