from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.common_schema import IInviteStatusEnum


class IInviteRead(BaseModel):
    uuid: UUID
    owner_avatar: str | None
    owner_full_name: str
    event_name: str
    event_until: datetime
    status: IInviteStatusEnum

    class Config:
        from_attributes = True
