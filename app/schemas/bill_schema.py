from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.models.bill_model import BillBase
from app.schemas.item_schema import IItemRead
from app.schemas.user_schema import IUserRead


class IBillCreate(BillBase):
    pass


class IBillRead(BillBase):
    uuid: UUID


class IBillResponse(BaseModel):
    uuid: UUID
    name: str
    total_price: float
    collected_price: float
    created_at: str
    until: str
    paid_by: IUserRead
    members: List[IUserRead]
    items: List[IItemRead]


class IBillUpdate(BillBase):
    pass
