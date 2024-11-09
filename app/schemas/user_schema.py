from uuid import UUID

from app.models.user_model import UserBase


class IUserCreate(UserBase):
    password: str


class IUserUpdate(UserBase):
    pass


class IUserRead(UserBase):
    uuid: UUID
