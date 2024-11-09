from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column
from sqlmodel import Field, String, Relationship

from app.models.base_model import BaseModel, BaseUUIDModel

if TYPE_CHECKING:
    from .event_model import Event
    from .user_model import User


class BillBase(BaseModel):
    name: str = Field(sa_column=Column(String(1000), index=True, unique=True, nullable=False))
    event_uuid: UUID | None = Field(default=None, foreign_key="event.uuid")


class Bill(BaseUUIDModel, BillBase, table=True):
    event: "Event" = Relationship(back_populates="bills", sa_relationship_kwargs={"lazy": "joined"})
    paid_by: "User" = Relationship(back_populates="bills", sa_relationship_kwargs={"lazy": "joined"})
