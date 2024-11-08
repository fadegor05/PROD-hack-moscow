from pydantic import FileUrl
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import Column
from sqlmodel import Field, String

from app.models.base_model import BaseModel, BaseUUIDModel


class UserBase(BaseModel):
    phone: PhoneNumber = Field(sa_column=Column(String(18), index=True, unique=True, nullable=False))
    avatar: FileUrl = Field(sa_column=Column(String(200), nullable=False))
    full_name: str = Field(sa_column=Column(String(100), nullable=False))


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str | None = Field(default=None, nullable=False)
