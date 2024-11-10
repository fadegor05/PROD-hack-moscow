from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app import crud
from app.models.bill_model import Bill
from app.models.item_model import Item
from app.models.user_model import User
from app.schemas.bill_schema import IBillResponse, IUserDebt
from app.schemas.common_schema import IOrderEnum
from app.schemas.item_schema import IItemRead
from app.schemas.user_schema import IUserRead


class BillService:
    def __init__(self):
        pass

    @staticmethod
    async def get_bill_prices(bill: Bill) -> tuple[Decimal, Decimal]:
        total_price = Decimal("0")
        collected_price = Decimal("0")
        for item in bill.items:
            total_price += Decimal(str(item.price))
            if item.is_paid:
                collected_price += Decimal(str(item.price))
        return total_price, collected_price

    @staticmethod
    async def get_bill_members(bill: Bill) -> List[User]:
        members = []
        for item in bill.items:
            if item.assigned_user not in members:
                members.append(item.assigned_user)
        return list(members)

    @staticmethod
    async def get_items_only_assigned_on_user_uuid(
        bill: Bill, user_uuid: UUID
    ) -> List[Item]:
        items = []
        for item in bill.items:
            if item.assigned_user_uuid == user_uuid:
                items.append(item)
        return items

    @staticmethod
    async def calculate_user_debts(bill: Bill) -> tuple[List[IUserDebt], float]:
        user_debts = {}
        total_debt = 0.0

        for item in bill.items:
            if item.assigned_user_uuid:
                amount = item.price / len(item.participants) if item.participants else 0
                if item.assigned_user_uuid not in user_debts:
                    user_debts[item.assigned_user_uuid] = 0
                user_debts[item.assigned_user_uuid] += amount
                total_debt += amount

        return [
            IUserDebt(user_uuid=user_uuid, amount=amount)
            for user_uuid, amount in user_debts.items()
        ], total_debt

    @staticmethod
    async def get_bill(
        bill_uuid: UUID, user_uuid: UUID, session: AsyncSession
    ) -> Optional[IBillResponse]:
        statement = (
            select(Bill)
            .where(Bill.uuid == bill_uuid)
            .options(selectinload(Bill.items))
        )
        
        result = await session.execute(statement)
        bill = result.scalar_one_or_none()
        
        if not bill:
            return None

        # Calculate debts for this bill
        user_debts, total_debt = await BillService.calculate_user_debts(bill)
        
        return IBillResponse(
            uuid=bill.uuid,
            name=bill.name,
            total_price=await BillService.get_bill_prices(bill)[0],
            collected_price=await BillService.get_bill_prices(bill)[1],
            created_at=bill.event.created_at.isoformat(),
            until=bill.event.until.isoformat(),
            paid_by=IUserRead.model_validate(bill.paid_by),
            members=[IUserRead.model_validate(member) for member in await BillService.get_bill_members(bill)],
            items=[IItemRead.model_validate(item) for item in bill.items],
            user_debts=user_debts,
            total_debt=total_debt
        )

    @staticmethod
    async def get_bills_for_user_multi_ordered(
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str,
        order: IOrderEnum = IOrderEnum.ascendent,
        session: AsyncSession,
        user_uuid: UUID,
    ):
        bills_uuid = await crud.bill.get_multi_ordered_uuids_for_user_uuid(
            skip=skip,
            limit=limit,
            order=order,
            order_by=order_by,
            session=session,
            user_uuid=user_uuid,
        )
        bills_uuid = set(bills_uuid)
        bills = []
        for bill_uuid in bills_uuid:
            bills.append(
                await BillService.get_bill(
                    bill_uuid=bill_uuid, user_uuid=user_uuid, session=session
                )
            )
        return bills
