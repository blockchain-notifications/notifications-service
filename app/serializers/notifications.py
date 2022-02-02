from pydantic import BaseModel


class Push(BaseModel):
    tx_hash: str
    sender: str
    recipient: str
    data: str
    event: str


class Ack(BaseModel):
    tx_hash: str


class AckResponse(BaseModel):
    tx_hash: str
    detail: str
    status: int
