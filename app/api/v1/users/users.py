from typing import Annotated, Union, List
from urllib.parse import unquote
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exception import MultiLangHTTPExceptions
from app.database.database import get_async_session
from app.schemas.common_schema import IOrderEnum
from app.schemas.user_schema import IUserCreate, IUserRead, IUserUpdate

users_router = APIRouter(prefix="/users", tags=["User"])


@users_router.get(
    "/{user_phone}",
    summary="Получить пользователя по номеру телефона",
    description="Возвращает информацию о пользователе по его номеру телефона",
    responses={
        404: {
            "description": "Пользователь не найден"
        }
    }
)
async def get_user_by_phone(user_phone: Annotated[str, Query],
                            session: AsyncSession = Depends(get_async_session)) -> IUserRead:
    decoded_phone = unquote(user_phone)
    user = await crud.user.get_by_phone(phone=decoded_phone, session=session)
    if user is None:
        raise MultiLangHTTPExceptions.USER_NOT_FOUND.to_exception()
    return user


@users_router.get(
    "/{user_uuid}",
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


@users_router.get("")
async def get_multi_users(skip: Annotated[Union[int, None], Query] = 0, limit: Annotated[Union[int, None], Query] = 100,
                          order_by: Annotated[Union[str, None], Query] = "uuid",
                          order: Annotated[Union[IOrderEnum, None], Query] = IOrderEnum.ascendent,
                          session: AsyncSession = Depends(get_async_session)) -> List[IUserRead]:
    users = await crud.user.get_multi_ordered(skip=skip, limit=limit, order_by=order_by, order=order, session=session)
    return users


@users_router.post(
    "",
    summary="Создать нового незарегистрированного пользователя",
    description="Создает новую незарегестрированную учетную запись пользователя",
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
