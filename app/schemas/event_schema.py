from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.models.event_model import EventBase
from app.schemas.bill_schema import IBillResponse
from app.schemas.user_schema import IUserRead


class IEventCreate(EventBase):
    pass


class IEventUpdate(EventBase):
    pass


class IEventRead(EventBase):
    uuid: UUID
    bills_uuid: List[UUID]


class IEventResponse(BaseModel):
    uuid: UUID
    name: str
    description: str
    created_at: str
    until: str
    total_price: float
    collected_price: float
    owner: IUserRead
    bills: List[IBillResponse]
