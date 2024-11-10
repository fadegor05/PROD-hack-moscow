import re
from typing import TYPE_CHECKING, List

from pydantic import field_validator
from sqlalchemy import Column
from sqlmodel import Field, String, Relationship

from app.models.base_model import BaseModel, BaseUUIDModel

if TYPE_CHECKING:
    from .bill_model import Bill
    from .event_model import Event
    from .item_model import Item
    from .invite_model import Invite


class UserBase(BaseModel):
    phone: str = Field(
        sa_column=Column(String(25), unique=True, nullable=False)
    )
    full_name: str = Field(sa_column=Column(String(100), nullable=False))

    @field_validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Invalid phone number")
        return v


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str | None = Field(default=None, nullable=True)
    paid: List["Bill"] = Relationship(back_populates="paid_by", sa_relationship_kwargs={"lazy": "selectin"})
    events: List["Event"] = Relationship(back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"})
    items: List["Item"] = Relationship(back_populates="assigned_user", sa_relationship_kwargs={"lazy": "selectin"})
    invites: List["Invite"] = Relationship(back_populates="invited", sa_relationship_kwargs={"lazy": "selectin"})
