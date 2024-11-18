from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas.common_schema import IOrderEnum
from app.schemas.event_schema import IEventResponse
from app.schemas.user_schema import IUserRead
from app.services.bill_service import BillService


class EventService:
    def __init__(self):
        pass

    @staticmethod
    async def get_event(event_uuid: UUID, user_uuid: UUID, session: AsyncSession) -> IEventResponse | None:
        event = await crud.event.get(uuid=event_uuid, session=session)
        bills = []
        total_price, collected_price = 0, 0
        for bill in event.bills:
            new_bill = await BillService.get_bill(bill_uuid=bill.uuid, user_uuid=user_uuid, session=session)
            total_price += new_bill.total_price
            collected_price += new_bill.collected_price
            bills.append(new_bill)

        if event is None:
            return None

        return IEventResponse(
            uuid=event.uuid,
            name=event.name,
            description=event.description,
            created_at=event.created_at.isoformat(),
            until=event.until.isoformat(),
            total_price=total_price,
            collected_price=collected_price,
            owner=IUserRead.model_validate(event.owner),
            bills=bills
        )

    @staticmethod
    async def get_events_for_user_multi_ordered(*, skip: int = 0, limit: int = 100, order_by: str,
                                                order: IOrderEnum = IOrderEnum.ascendent, session: AsyncSession,
                                                user_uuid: UUID):
        events_uuid = await crud.event.get_multi_ordered_uuids_for_user_uuid(skip=skip, limit=limit, order=order,
                                                                             order_by=order_by,
                                                                             session=session, user_uuid=user_uuid)
        events_uuid = set(events_uuid)
        events = []
        for event_uuid in events_uuid:
            events.append(await EventService.get_event(event_uuid=event_uuid, user_uuid=user_uuid, session=session))
        return events
