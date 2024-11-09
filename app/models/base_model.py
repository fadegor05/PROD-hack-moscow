from uuid import uuid4, UUID

from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseUUIDModel(BaseModel):
    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
