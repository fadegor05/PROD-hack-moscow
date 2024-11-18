from uuid import UUID

from pydantic import BaseModel

from app.models.item_model import ItemBase


class IItemCreate(ItemBase):
    pass


class IItemRead(ItemBase):
    uuid: UUID


class IItemUpdate(ItemBase):
    pass


class IItemResponse(BaseModel):
    uuid: UUID
