from typing import Annotated, Union, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exception import MultiLangHTTPExceptions
from app.database.database import get_async_session
from app.schemas.bill_schema import IBillRead, IBillCreate
from app.schemas.common_schema import IOrderEnum

bills_router = APIRouter(prefix="/bills", tags=["Bill"])


@bills_router.get("/{bill_uuid}")
async def get_bill_by_uuid(bill_uuid: UUID, session: AsyncSession = Depends(get_async_session)) -> IBillRead:
    event = await crud.bill.get_with_uuid_columns(uuid=bill_uuid, session=session, columns=["items"],
                                                  read_interface=IBillRead)
    if event is None:
        raise MultiLangHTTPExceptions.BILL_NOT_FOUND.to_exception()
    return event


@bills_router.get("")
async def get_multi_bills(skip: Annotated[Union[int, None], Query] = 0,
                          limit: Annotated[Union[int, None], Query] = 20,
                          order_by: Annotated[Union[str, None], Query] = "uuid",
                          order: Annotated[Union[IOrderEnum, None], Query] = IOrderEnum.ascendent,
                          session: AsyncSession = Depends(get_async_session)) -> List[IBillRead]:
    events = await crud.bill.get_multi_ordered_with_uuid_columns(skip=skip, limit=limit, order_by=order_by, order=order,
                                                                 session=session, columns=["items"],
                                                                 read_interface=IBillRead)
    return events


@bills_router.post("")
async def post_bill(user_data: IBillCreate, session: AsyncSession = Depends(get_async_session)) -> IBillRead:
    try:
        bill = await crud.bill.create(obj_in=user_data, session=session)
    except HTTPException:
        raise MultiLangHTTPExceptions.BILL_ALREADY_EXISTS.to_exception()
    bill_new = await crud.bill.get_with_uuid_columns(uuid=bill.uuid, session=session, columns=["items"],
                                                     read_interface=IBillRead)
    return bill_new
