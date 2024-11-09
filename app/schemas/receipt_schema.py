from typing import List

from pydantic import BaseModel


class IReceiptItem(BaseModel):
    name: str
    price: float
    quantity: float


class IReceiptRead(BaseModel):
    store: str
    items: List[IReceiptItem]
    total: float
    category: str | None


class IQRCodePost(BaseModel):
    qr_raw: str
