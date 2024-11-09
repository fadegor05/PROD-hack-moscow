from uuid import UUID

from app.models.bill_model import BillBase


class IBillCreate(BillBase):
    pass


class IBillRead(BillBase):
    uuid: UUID


class IBillUpdate(BillBase):
    pass
