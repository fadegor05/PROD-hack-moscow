from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String
from sqlmodel import Field, Column, Relationship

from app.models.base_model import BaseModel, BaseUUIDModel

if TYPE_CHECKING:
    from .user_model import User
    from .bill_model import Bill


class ItemBase(BaseModel):
    name: str = Field(sa_column=Column(String(50), index=True, unique=True, nullable=False))
    price: float = Field(default=0, nullable=False)
    assigned_user_uuid: UUID = Field(default=None, foreign_key="user.uuid")
    bill_uuid: UUID = Field(default=None, foreign_key="bill.uuid")
    is_paid: bool = Field(default=False, nullable=False)


class Item(BaseUUIDModel, ItemBase, table=True):
    assigned_user: "User" = Relationship(back_populates="items", sa_relationship_kwargs={"lazy": "selectin"})
    bill: "Bill" = Relationship(back_populates="items", sa_relationship_kwargs={"lazy": "selectin"})
