import re

from pydantic import FileUrl, field_validator
from sqlalchemy import Column
from sqlmodel import Field, String

from app.models.base_model import BaseModel, BaseUUIDModel


class UserBase(BaseModel):
    phone: str = Field(sa_column=Column(String(25), index=True, unique=True, nullable=False))
    avatar: FileUrl | None = Field(default=None, sa_column=Column(String(200), nullable=True))
    full_name: str = Field(sa_column=Column(String(100), nullable=False))

    @field_validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Невалидный номер телефона")
        return v


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str | None = Field(default=None, nullable=False)
