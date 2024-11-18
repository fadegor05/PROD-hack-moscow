from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.base_model import BaseModel, BaseUUIDModel

if TYPE_CHECKING:
    from .event_model import Event
    from .user_model import User


class InviteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class InviteBase(BaseModel):
    event_uuid: UUID = Field(foreign_key="event.uuid")
    invited_uuid: UUID = Field(foreign_key="user.uuid")
    status: InviteStatus = Field(default=InviteStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)


class Invite(BaseUUIDModel, InviteBase, table=True):
    event: "Event" = Relationship(
        back_populates="invites", sa_relationship_kwargs={"lazy": "selectin"}
    )
    invited: "User" = Relationship(
        back_populates="invites", sa_relationship_kwargs={"lazy": "selectin"}
    )
