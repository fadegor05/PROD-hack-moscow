from uuid import UUID

from pydantic_partial import create_partial_model

from app.models.user_model import UserBase


class IUserCreate(UserBase):
    password: str


IUserUpdate = create_partial_model(UserBase)


class IUserRead(UserBase):
    uuid: UUID
