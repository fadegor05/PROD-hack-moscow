from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.bill_model import Bill
from app.models.item_model import Item
from app.models.user_model import User
from app.schemas.bill_schema import IBillResponse
from app.schemas.common_schema import IOrderEnum
from app.schemas.item_schema import IItemRead
from app.schemas.user_schema import IUserRead


class BillService:
    def __init__(self):
        pass

    @staticmethod
    async def get_bill_prices(bill: Bill) -> (float, float):
        total_price = 0
        collected_price = 0
        for item in bill.items:
            total_price += item.price
            if item.is_paid:
                collected_price += item.price
        return total_price, collected_price

    @staticmethod
    async def get_bill_members(bill: Bill) -> List[User]:
        members = []
        for item in bill.items:
            if item.assigned_user not in members:
                members.append(item.assigned_user)
        return list(members)

    @staticmethod
    async def get_items_only_assigned_on_user_uuid(bill: Bill, user_uuid: UUID) -> List[Item]:
        items = []
        for item in bill.items:
            if item.assigned_user_uuid == user_uuid:
                items.append(item)
        return items

    @staticmethod
    async def get_bill(bill_uuid: UUID, user_uuid: UUID, session: AsyncSession) -> IBillResponse | None:
        bill = await crud.bill.get(uuid=bill_uuid, session=session)
        if bill is None:
            return None
        event = bill.event
        total_price, collected_price = await BillService.get_bill_prices(bill=bill)
        paid_by = bill.paid_by
        members = await BillService.get_bill_members(bill=bill)
        items = bill.items
        if paid_by.uuid != user_uuid:
            items = await BillService.get_items_only_assigned_on_user_uuid(bill=bill, user_uuid=user_uuid)

        return IBillResponse(
            uuid=bill.uuid,
            name=bill.name,
            total_price=total_price,
            collected_price=collected_price,
            created_at=event.created_at.isoformat(),
            until=event.until.isoformat(),
            paid_by=IUserRead.model_validate(paid_by),
            members=[IUserRead.model_validate(member) for member in members],
            items=[IItemRead.model_validate(item) for item in items]
        )

    @staticmethod
    async def get_bills_for_user_multi_ordered(*, skip: int = 0, limit: int = 100, order_by: str,
                                               order: IOrderEnum = IOrderEnum.ascendent, session: AsyncSession,
                                               user_uuid: UUID):
        bills_uuid = await crud.bill.get_multi_ordered_uuids_for_user_uuid(skip=skip, limit=limit, order=order,
                                                                           order_by=order_by,
                                                                           session=session, user_uuid=user_uuid)
        bills_uuid = set(bills_uuid)
        bills = []
        for bill_uuid in bills_uuid:
            bills.append(await BillService.get_bill(bill_uuid=bill_uuid, user_uuid=user_uuid, session=session))
        return bills
