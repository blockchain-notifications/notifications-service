import datetime
from pydantic import BaseModel


class Channel(BaseModel):
    name: str
    tx_hash: str
    url: str


class Notification(BaseModel):
    channel: Channel
    client_id: str
    id: int
    title: str
    text: str
    created_at: datetime.datetime
