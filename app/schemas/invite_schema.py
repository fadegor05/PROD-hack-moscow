from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class InviteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class IInviteBase(BaseModel):
    event_uuid: UUID
    user_uuid: UUID
    status: InviteStatus


class IInviteCreate(IInviteBase):
    pass


class IInviteUpdate(BaseModel):
    status: InviteStatus


class IInviteRead(IInviteBase):
    uuid: UUID

    class Config:
        from_attributes = True


class IInviteRequest(BaseModel):
    invite_uuid: UUID


class ICreateInviteRequest(BaseModel):
    event_uuid: UUID
    user_uuid: UUID
