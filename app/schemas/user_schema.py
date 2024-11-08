from uuid import UUID

from pydantic import ConfigDict

from app.models.user_model import UserBase


class IUserCreate(UserBase):
    model_config = ConfigDict()
    password: str
    hashed_password: str | None = None


class IUserUpdate(UserBase):
    pass


class IUserRead(UserBase):
    uuid: UUID
