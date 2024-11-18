from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import Column
from sqlmodel import Field, String, Relationship

from app.models.base_model import BaseModel, BaseUUIDModel

if TYPE_CHECKING:
    from .bill_model import Bill
    from .user_model import User
    from .invite_model import Invite


class EventBase(BaseModel):
    name: str = Field(sa_column=Column(String(120), nullable=False))
    description: str | None = Field(default=None, sa_column=Column(String(200)))
    created_at: datetime | None = Field(default_factory=datetime.now)
    until: datetime | None = Field(default_factory=datetime.now)
    owner_uuid: UUID = Field(default=None, foreign_key="user.uuid")


class Event(BaseUUIDModel, EventBase, table=True):
    bills: List["Bill"] = Relationship(back_populates="event", sa_relationship_kwargs={"lazy": "selectin"})
    owner: "User" = Relationship(back_populates="events", sa_relationship_kwargs={"lazy": "selectin"})
    invites: List["Invite"] = Relationship(back_populates="event", sa_relationship_kwargs={"lazy": "selectin"})
