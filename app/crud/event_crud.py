from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from sqlalchemy.orm import aliased
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import BaseCRUD, ModelType
from app.models.bill_model import Bill
from app.models.event_model import Event
from app.models.item_model import Item
from app.schemas.common_schema import IOrderEnum
from app.schemas.event_schema import IEventCreate, IEventUpdate


class EventCRUD(BaseCRUD[Event, IEventCreate, IEventUpdate]):
    async def create(self, *, obj_in: IEventCreate | Event, session: AsyncSession) -> Event:
        now = datetime.now()
        until = now + timedelta(days=1)
        obj_in.created_at = now
        obj_in.until = until
        return await super().create(obj_in=obj_in, session=session)

    async def get_multi_ordered_uuids_for_user_uuid(self, *, skip: int = 0,
                                                    limit: int = 100, order_by: str = "created_at",
                                                    order: IOrderEnum = IOrderEnum.ascendent,
                                                    session: AsyncSession, user_uuid: UUID) -> List[ModelType]:
        columns = self.model.__table__.columns

        if order_by is None or order_by not in columns:
            order_by = "uuid"

        bill_alias = aliased(Bill)
        item_alias = aliased(Item)

        query = (
            select(self.model.uuid)
            .join(bill_alias, self.model.bills)
            .join(item_alias, bill_alias.items)
            .where(item_alias.assigned_user_uuid == user_uuid)
            .offset(skip)
            .limit(limit)
        )

        if order == IOrderEnum.ascendent:
            query = query.order_by(columns[order_by].asc())
        else:
            query = query.order_by(columns[order_by].desc())

        response = await session.execute(query)
        return response.scalars().all()


event = EventCRUD(Event)
