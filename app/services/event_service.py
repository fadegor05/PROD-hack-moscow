from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app import crud
from app.models.event_model import Event
from app.schemas.bill_schema import IUserDebt
from app.schemas.common_schema import IOrderEnum
from app.schemas.event_schema import IEventResponse
from app.schemas.user_schema import IUserRead
from app.services.bill_service import BillService


class EventService:
    def __init__(self):
        pass

    @staticmethod
    async def get_event(event_uuid: UUID, user_uuid: UUID, session: AsyncSession) -> Optional[IEventResponse]:
        statement = (
            select(Event)
            .where(Event.uuid == event_uuid)
            .options(selectinload(Event.bills))
        )
        
        result = await session.execute(statement)
        event = result.scalar_one_or_none()
        
        if not event:
            return None

        bills = []
        total_debt = Decimal("0")
        
        for bill in event.bills:
            bill_response = await BillService.get_bill(
                bill_uuid=bill.uuid,
                user_uuid=user_uuid,
                session=session
            )
            if bill_response:
                bills.append(bill_response)
                total_debt += bill_response.total_debt

        return IEventResponse(
            uuid=event.uuid,
            title=event.title,
            created_at=event.created_at.isoformat(),
            until=event.until.isoformat(),
            owner=IUserRead.model_validate(event.owner),
            members=[IUserRead.model_validate(member) for member in event.members],
            bills=bills,
            total_debt=total_debt
        )

    @staticmethod
    async def get_events_for_user_multi_ordered(
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str,
        order: IOrderEnum = IOrderEnum.ascendent,
        session: AsyncSession,
        user_uuid: UUID,
    ) -> List[IEventResponse]:
        events_uuid = await crud.event.get_multi_ordered_uuids_for_user_uuid(
            skip=skip,
            limit=limit,
            order=order,
            order_by=order_by,
            session=session,
            user_uuid=user_uuid,
        )
        events_uuid = set(events_uuid)
        events = []
        for event_uuid in events_uuid:
            event = await EventService.get_event(
                event_uuid=event_uuid,
                user_uuid=user_uuid,
                session=session
            )
            if event:
                events.append(event)
        return events
