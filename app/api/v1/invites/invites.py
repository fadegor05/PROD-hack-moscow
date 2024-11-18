from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database.database import get_async_session
from app.schemas.invite_schema import (
    IInviteRead,
    ICreateInviteRequest,
    IInviteRequest,
)
from app.services.invite_service import InviteService


invites_router = APIRouter(prefix="/invites", tags=["Invites"])


@invites_router.post(
    "/create",
    status_code=201,
    summary="Создать приглашение",
    description="Создать приглашение для пользователя присоединиться к событию",
)
async def create_invite(
    request: ICreateInviteRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> IInviteRead:
    return await InviteService.create_invite(
        event_uuid=request.event_uuid, user_uuid=request.user_uuid, session=session
    )


@invites_router.post(
    "/accept",
    summary="Принять приглашение",
    description="Принять приглашение присоединиться к событию",
)
async def accept_invite(
    request: IInviteRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> IInviteRead:
    return await InviteService.accept_invite(
        invite_uuid=request.invite_uuid, user_uuid=current_user.uuid, session=session
    )


@invites_router.post(
    "/decline",
    summary="Отклонить приглашение",
    description="Отклонить приглашение присоединиться к событию",
)
async def decline_invite(
    request: IInviteRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> IInviteRead:
    return await InviteService.decline_invite(
        invite_uuid=request.invite_uuid, user_uuid=current_user.uuid, session=session
    )
