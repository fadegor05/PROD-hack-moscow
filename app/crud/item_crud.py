from app.crud.base_crud import BaseCRUD
from app.models.item_model import Item
from app.schemas.item_schema import IItemCreate, IItemUpdate


class ItemCRUD(BaseCRUD[Item, IItemCreate, IItemUpdate]):
    pass


item = ItemCRUD(Item)
