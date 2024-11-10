from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.event_model import EventBase
from app.schemas.bill_schema import IBillResponse
from app.schemas.user_schema import IUserRead


class IEventCreate(EventBase):
    owner_uuid: None = None


class IEventRead(BaseModel):
    uuid: UUID
    title: str
    bills_uuid: Optional[List[UUID]] = None
    model_config = ConfigDict(from_attributes=True)


class IEventResponse(BaseModel):
    uuid: UUID
    title: str
    created_at: str
    until: str
    owner: IUserRead
    members: List[IUserRead]
    bills: List[IBillResponse]
    total_debt: Decimal


class IEventUpdate(EventBase):
    pass
