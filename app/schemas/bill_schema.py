from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.bill_model import BillBase
from app.schemas.item_schema import IItemRead
from app.schemas.user_schema import IUserRead


class IUserDebt(BaseModel):
    user_uuid: UUID
    amount: Decimal


class IBillCreate(BillBase):
    pass


class IBillRead(BaseModel):
    uuid: UUID
    event_uuid: UUID
    title: str
    items_uuid: Optional[List[UUID]] = None
    user_debts: List[IUserDebt]
    total_debt: float
    model_config = ConfigDict(from_attributes=True)


class IBillResponse(BaseModel):
    uuid: UUID
    name: str
    total_price: Decimal
    collected_price: Decimal
    created_at: str
    until: str
    paid_by: IUserRead
    members: List[IUserRead]
    items: List[IItemRead]
    user_debts: List[IUserDebt]
    total_debt: Decimal


class IBillUpdate(BillBase):
    pass
