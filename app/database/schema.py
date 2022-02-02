from pydantic import BaseModel


class Notification(BaseModel):
    tx_hash: str
    sender: str
    recipient: str
    data: str
    event: str
    is_read: bool
