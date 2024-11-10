from typing import Annotated, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.deps import get_current_user
from app.core.exception import MultiLangHTTPExceptions
from app.database.database import get_async_session
from app.schemas.bill_schema import IBillRead, IBillCreate, IBillResponse
from app.schemas.common_schema import IOrderEnum
from app.services.bill_service import BillService

bills_router = APIRouter(prefix="/bills", tags=["Bill"])


@bills_router.get("/{bill_uuid}")
async def get_bill_by_uuid(bill_uuid: UUID, session: AsyncSession = Depends(get_async_session),
                           current_user=Depends(get_current_user)) -> IBillResponse:
    bill = await BillService.get_bill(bill_uuid=bill_uuid, session=session,
                                      user_uuid=current_user.uuid)
    if bill is None:
        raise MultiLangHTTPExceptions.BILL_NOT_FOUND.to_exception()
    return bill


@bills_router.get("")
async def get_multi_bills(skip: Annotated[Union[int, None], Query] = 0,
                          limit: Annotated[Union[int, None], Query] = 20,
                          order_by: Annotated[Union[str, None], Query] = "uuid",
                          order: Annotated[Union[IOrderEnum, None], Query] = IOrderEnum.ascendent,
                          session: AsyncSession = Depends(get_async_session),
                          current_user=Depends(get_current_user)):
    bills = await BillService.get_bills_for_user_multi_ordered(skip=skip, limit=limit, order_by=order_by, order=order,
                                                               session=session,
                                                               user_uuid=current_user.uuid)
    return bills


@bills_router.post("")
async def post_bill(user_data: IBillCreate, session: AsyncSession = Depends(get_async_session),
                    current_user=Depends(get_current_user)) -> IBillRead:
    try:
        bill = await crud.bill.create(obj_in=user_data, session=session)
    except HTTPException:
        raise MultiLangHTTPExceptions.BILL_ALREADY_EXISTS.to_exception()
    bill_new = await crud.bill.get_with_uuid_columns(uuid=bill.uuid, session=session, columns=["items"],
                                                     read_interface=IBillRead)
    return bill_new
