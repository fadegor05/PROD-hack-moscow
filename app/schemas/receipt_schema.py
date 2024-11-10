from typing import List
from decimal import Decimal
from pydantic import BaseModel


class IReceiptItem(BaseModel):
    name: str
    price: Decimal
    quantity: Decimal


class IReceiptRead(BaseModel):
    store: str
    items: List[IReceiptItem]
    total: Decimal
    category: str | None


class IQRCodePost(BaseModel):
    qr_raw: str
