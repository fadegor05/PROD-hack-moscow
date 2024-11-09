from app.crud.base_crud import BaseCRUD
from app.models.bill_model import Bill
from app.schemas.bill_schema import IBillCreate, IBillUpdate


class BillCRUD(BaseCRUD[Bill, IBillCreate, IBillUpdate]):
    pass


bill = BillCRUD(Bill)
