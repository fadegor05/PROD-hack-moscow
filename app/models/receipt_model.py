from datetime import datetime
from typing import List
from decimal import Decimal
from sqlmodel import Field, Relationship
from app.models.base_model import BaseUUIDModel
from app.models.receipt_item_model import ReceiptItem


class Receipt(BaseUUIDModel, table=True):
    store: str = Field(index=True)
    total: Decimal = Field(default=0, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    items: List["ReceiptItem"] = Relationship(back_populates="receipt")
