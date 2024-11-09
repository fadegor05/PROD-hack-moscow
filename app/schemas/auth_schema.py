from pydantic import BaseModel, Field


class ILogin(BaseModel):
    """Schema for login credentials"""

    phone: str = Field(
        ...,
        description="User phone number in international format (e.g. +79123456789)",
        example="+79123456789",
    )
    password: str = Field(
        ..., description="User password", min_length=8, example="strongpassword123"
    )


class IToken(BaseModel):
    """Schema for JWT token response"""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
