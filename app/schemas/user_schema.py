from uuid import UUID

from pydantic import BaseModel, Field


class IUserBase(BaseModel):
    """Base user schema with common fields"""
    phone: str = Field(
        ...,
        description="User phone number in international format",
        example="+79123456789"
    )
    full_name: str = Field(
        ...,
        description="User's full name",
        example="John Doe",
        min_length=2,
        max_length=100
    )


class IUserCreate(IUserBase):
    pass


class IUserRegister(IUserBase):
    """Schema for creating a new user"""
    password: str = Field(
        ...,
        description="User password",
        min_length=8,
        example="strongpassword123"
    )


class IUserUpdate(BaseModel):
    """Schema for updating user information"""
    full_name: str | None = Field(
        None,
        description="New full name",
        example="John Smith"
    )


class IUserRead(IUserBase):
    """Schema for reading user information"""
    uuid: UUID = Field(..., description="User's unique identifier")

    class Config:
        from_attributes = True
