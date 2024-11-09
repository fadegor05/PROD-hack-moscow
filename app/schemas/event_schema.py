from typing import List
from uuid import UUID

from app.models.event_model import EventBase


class IEventCreate(EventBase):
    pass


class IEventUpdate(EventBase):
    pass


class IEventRead(EventBase):
    uuid: UUID
    bills_uuid: List[UUID]
