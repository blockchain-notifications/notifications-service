from json import JSONDecodeError
from typing import List, Optional

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.database.postgres import notifications, engine
from app.services.manager import manager
from app.serializers.notifications import Push, Ack, AckResponse, PushReadOnly

notifications_router = APIRouter()


@notifications_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            try:
                data = await websocket.receive_json()
            except JSONDecodeError:
                continue

            try:
                ack = Ack.parse_obj(data)
            except (TypeError, KeyError, ValidationError):
                continue

            noty = engine.execute(
                notifications.select().where(notifications.c.tx_hash == ack.tx_hash)
            ).first()

            if not noty:
                response = AckResponse.parse_obj(
                    {
                        "status": 404,
                        "detail": "This push-notification does not exist",
                        "tx_hash": ack.tx_hash,
                    }
                )
                await manager.send_personal_message(response, client_id)
                continue

            engine.execute(
                notifications.update()
                .where(notifications.c.tx_hash == ack.tx_hash)
                .values(is_read=True)
            )
            response = AckResponse.parse_obj(
                {"status": 200, "detail": "Acknowledged", "tx_hash": ack.tx_hash}
            )
            await manager.send_personal_message(response, client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)


@notifications_router.get("/notifications/")
async def push_read(client_id: str, is_read: Optional[bool] = None) -> List[Push]:
    if is_read is None:
        pushes = engine.execute(
            notifications.select().where(notifications.c.recipient == client_id)
        )
    else:
        pushes = engine.execute(
            notifications.select().where(
                notifications.c.recipient == client_id,
                notifications.c.is_read == is_read,
            )
        )

    return list(map(lambda push: PushReadOnly.parse_obj(push), pushes))


@notifications_router.post("/notifications/")
async def push_send(push: Push):
    noty_exists = engine.execute(
        notifications.select().where(notifications.c.tx_hash == push.tx_hash)
    ).first()

    if not noty_exists:
        engine.execute(
            notifications.insert().values(**{**push.__dict__, "is_read": False})
        )

    response = {"status": "ok"}
    try:
        if push.recipient in manager.active_connections:
            await manager.send_personal_message(push, push.recipient)
    except WebSocketDisconnect:
        response["status"] = "disconnected"
    return response
