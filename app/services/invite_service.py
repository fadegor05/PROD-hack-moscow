from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exception import MultiLangHTTPExceptions
from app.schemas.invite_schema import IInviteCreate, IInviteRead


class InviteService:
    @staticmethod
    async def create_invite(
        event_uuid: UUID, user_uuid: UUID, session: AsyncSession
    ) -> IInviteRead:
        event = await crud.event.get(uuid=event_uuid, session=session)
        if not event:
            raise MultiLangHTTPExceptions.EVENT_NOT_FOUND.to_exception()

        user = await crud.user.get(uuid=user_uuid, session=session)
        if not user:
            raise MultiLangHTTPExceptions.USER_NOT_FOUND.to_exception()

        invite_data = IInviteCreate(
            event_uuid=event_uuid, user_uuid=user_uuid, status="pending"
        )

        invite = await crud.invite.create(obj_in=invite_data, session=session)
        return invite

    @staticmethod
    async def accept_invite(
        invite_uuid: UUID, user_uuid: UUID, session: AsyncSession
    ) -> IInviteRead:
        invite = await crud.invite.get(uuid=invite_uuid, session=session)
        if not invite:
            raise MultiLangHTTPExceptions.INVITE_NOT_FOUND.to_exception()

        if invite.user_uuid != user_uuid:
            raise MultiLangHTTPExceptions.INVALID_PERMISSIONS.to_exception()

        updated_invite = await crud.invite.update(
            obj_current=invite, obj_new={"status": "accepted"}, session=session
        )

        return updated_invite

    @staticmethod
    async def decline_invite(
        invite_uuid: UUID, user_uuid: UUID, session: AsyncSession
    ) -> IInviteRead:
        invite = await crud.invite.get(uuid=invite_uuid, session=session)
        if not invite:
            raise MultiLangHTTPExceptions.INVITE_NOT_FOUND.to_exception()

        if invite.user_uuid != user_uuid:
            raise MultiLangHTTPExceptions.INVALID_PERMISSIONS.to_exception()

        updated_invite = await crud.invite.update(
            obj_current=invite, obj_new={"status": "declined"}, session=session
        )

        return updated_invite
