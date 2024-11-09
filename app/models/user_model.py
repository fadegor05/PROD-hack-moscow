import re

from pydantic import field_validator
from sqlalchemy import Column
from sqlmodel import Field, String

from app.models.base_model import BaseModel, BaseUUIDModel


class UserBase(BaseModel):
    phone: str = Field(
        sa_column=Column(String(25), index=True, unique=True, nullable=False)
    )
    full_name: str = Field(sa_column=Column(String(100), nullable=False))

    @field_validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Invalid phone number")
        return v


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str = Field(default=None, nullable=False)
