from typing import Annotated, Union, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.deps import get_current_user
from app.core.exception import MultiLangHTTPExceptions
from app.database.database import get_async_session
from app.schemas.common_schema import IOrderEnum
from app.schemas.item_schema import IItemCreate, IItemRead

items_router = APIRouter(prefix="/items", tags=["Item"])


@items_router.get("/{item_uuid}")
async def get_item_by_uuid(item_uuid: UUID, session: AsyncSession = Depends(get_async_session),
                           current_user=Depends(get_current_user)) -> IItemRead:
    event = await crud.item.get_with_uuid_columns(uuid=item_uuid, session=session, columns=["items"],
                                                  read_interface=IItemRead)
    if event is None:
        raise MultiLangHTTPExceptions.ITEM_NOT_FOUND.to_exception()
    return event


@items_router.get("")
async def get_multi_bills(skip: Annotated[Union[int, None], Query] = 0,
                          limit: Annotated[Union[int, None], Query] = 20,
                          order_by: Annotated[Union[str, None], Query] = "uuid",
                          order: Annotated[Union[IOrderEnum, None], Query] = IOrderEnum.ascendent,
                          session: AsyncSession = Depends(get_async_session),
                          current_user=Depends(get_current_user)) -> List[IItemRead]:
    events = await crud.item.get_multi_bills(skip=skip, limit=limit, order_by=order_by, order=order, session=session)
    return events


@items_router.post("")
async def post_item(user_data: IItemCreate, session: AsyncSession = Depends(get_async_session),
                    current_user=Depends(get_current_user)) -> IItemRead:
    try:
        bill = await crud.item.create(obj_in=user_data, session=session)
    except HTTPException:
        raise MultiLangHTTPExceptions.ITEM_ALREADY_EXISTS.to_exception()
    return bill
