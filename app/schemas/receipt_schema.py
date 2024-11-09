from typing import List
from pydantic import BaseModel


class ReceiptItem(BaseModel):
    name: str
    price: float
    quantity: float


class ReceiptInfo(BaseModel):
    store: str
    items: List[ReceiptItem]
    total: float


class QRCodeInput(BaseModel):
    qr_raw: str 