from datetime import datetime, timedelta

from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import BaseCRUD
from app.models.event_model import Event
from app.schemas.event_schema import IEventCreate, IEventUpdate


class EventCRUD(BaseCRUD[Event, IEventCreate, IEventUpdate]):
    async def create(self, *, obj_in: IEventCreate | Event, session: AsyncSession) -> Event:
        now = datetime.now()
        until = now + timedelta(days=1)
        obj_in.created_at = now
        obj_in.until = until
        return await super().create(obj_in=obj_in, session=session)


event = EventCRUD(Event)
