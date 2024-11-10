from typing import Annotated, Union, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.deps import get_current_user
from app.core.exception import MultiLangHTTPExceptions
from app.database.database import get_async_session
from app.schemas.common_schema import IOrderEnum
from app.schemas.event_schema import IEventRead, IEventCreate, IEventResponse
from app.services.event_service import EventService

events_router = APIRouter(prefix="/events", tags=["Event"])


@events_router.get("/{event_uuid}")
async def get_event_by_uuid(event_uuid: UUID, session: AsyncSession = Depends(get_async_session),
                            current_user=Depends(get_current_user)) -> IEventResponse:
    event = await EventService.get_event(event_uuid=event_uuid, session=session,
                                         user_uuid=current_user.uuid)
    if event is None:
        raise MultiLangHTTPExceptions.EVENT_NOT_FOUND.to_exception()
    return event


@events_router.get("")
async def get_multi_events(skip: Annotated[Union[int, None], Query] = 0,
                           limit: Annotated[Union[int, None], Query] = 20,
                           order_by: Annotated[Union[str, None], Query] = "uuid",
                           order: Annotated[Union[IOrderEnum, None], Query] = IOrderEnum.ascendent,
                           session: AsyncSession = Depends(get_async_session),
                           current_user=Depends(get_current_user)) -> List[IEventResponse]:
    events = await EventService.get_events_for_user_multi_ordered(skip=skip, limit=limit, order_by=order_by,
                                                                  order=order, session=session,
                                                                  user_uuid=current_user.uuid)
    return events


@events_router.post("")
async def post_event(user_data: IEventCreate, session: AsyncSession = Depends(get_async_session),
                     current_user=Depends(get_current_user)) -> IEventRead:
    try:
        event = await crud.event.create(obj_in=user_data, session=session)
    except HTTPException:
        raise MultiLangHTTPExceptions.EVENT_ALREADY_EXISTS.to_exception()
    event_new = await crud.event.get_with_uuid_columns(uuid=event.uuid, session=session, columns=["bills"],
                                                       read_interface=IEventRead)
    return event_new
