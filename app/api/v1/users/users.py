from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exception import MultiLangHTTPExceptions
from app.database.database import get_async_session
from app.schemas.user_schema import IUserCreate, IUserRead, IUserUpdate

users_router = APIRouter(prefix="/users", tags=["User"])


@users_router.get(
    "/{user_uuid}",
    response_model=IUserRead,
    summary="Получить пользователя по UUID",
    description="Возвращает информацию о пользователе по его UUID",
    responses={
        404: {
            "description": "Пользователь не найден",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "en": "User not found",
                            "ru": "Пользователь не найден"
                        }
                    }
                }
            }
        }
    }
)
async def get_user_by_uuid(user_uuid: UUID, session: AsyncSession = Depends(get_async_session)) -> IUserRead:
    user = await crud.user.get(uuid=user_uuid, session=session)
    if user is None:
        raise MultiLangHTTPExceptions.USER_NOT_FOUND.to_exception()
    return user


@users_router.get(
    "/{user_phone}",
    response_model=IUserRead,
    summary="Получить пользователя по номеру телефона",
    description="Возвращает информацию о пользователе по его номеру телефона",
    responses={
        404: {
            "description": "Пользователь не найден"
        }
    }
)
async def get_user_by_phone(user_phone: str, session: AsyncSession = Depends(get_async_session)) -> IUserRead:
    user = await crud.user.get_by_phone(phone=user_phone, session=session)
    if user is None:
        raise MultiLangHTTPExceptions.USER_NOT_FOUND.to_exception()
    return user


@users_router.get("")
async def get_users():
    # TODO
    ...


@users_router.post(
    "",
    response_model=IUserRead,
    summary="Создать нового пользователя",
    description="Создает новую учетную запись пользователя",
    responses={
        409: {
            "description": "Пользователь уже существует"
        }
    }
)
async def post_user(user_data: IUserCreate, session: AsyncSession = Depends(get_async_session)) -> IUserRead:
    try:
        user = await crud.user.create(obj_in=user_data, session=session)
    except HTTPException:
        raise MultiLangHTTPExceptions.USER_ALREADY_EXISTS.to_exception()
    return user


@users_router.patch(
    "/{user_uuid}",
    response_model=IUserRead,
    summary="Обновить данные пользователя",
    description="Обновляет информацию о существующем пользователе",
    responses={
        404: {
            "description": "Пользователь не найден"
        }
    }
)
async def patch_user_by_uuid(user_uuid: UUID, user_data: IUserUpdate,
                             session: AsyncSession = Depends(get_async_session)) -> IUserRead:
    user = await crud.user.get(uuid=user_uuid, session=session)
    if user is None:
        raise MultiLangHTTPExceptions.USER_NOT_FOUND.to_exception()
    updated_user = await crud.user.update(obj_current=user, obj_new=user_data, session=session)
    return updated_user


@users_router.delete(
    "/{user_uuid}",
    response_model=IUserRead,
    summary="Удалить пользователя",
    description="Удаляет существующего пользователя",
    responses={
        404: {
            "description": "Пользователь не найден"
        }
    }
)
async def delete_user_by_uuid(user_uuid: UUID, session: AsyncSession = Depends(get_async_session)) -> IUserRead:
    user = await crud.user.remove(uuid=user_uuid, session=session)
    if user is None:
        raise MultiLangHTTPExceptions.USER_NOT_FOUND.to_exception()
    return user
