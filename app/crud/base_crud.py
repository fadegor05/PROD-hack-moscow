from typing import TypeVar, Generic, List, Any
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(self, *, uuid: UUID | str, session: AsyncSession) -> ModelType | None:
        statement = select(self.model).where(self.model.uuid == uuid)
        response = await session.execute(statement)
        return response.scalar_one_or_none()

    async def get_by_uuids(self, *, list_uuids: List[UUID | str], session: AsyncSession) -> List[ModelType]:
        statement = select(self.model).where(self.model.uuid.in_(list_uuids))
        response = await session.execute(statement)
        return response.scalars().all()

    async def create(self, *, obj_in: CreateSchemaType | ModelType, session: AsyncSession) -> ModelType:
        db_obj = self.model.model_validate(obj_in)

        try:
            session.add(db_obj)
            await session.commit()
        except:
            await session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Данный ресурс уже существует",
            )
        await session.refresh(db_obj)
        return db_obj

    async def update(self, *, obj_current: ModelType,
                     obj_new: UpdateSchemaType | dict[str, Any] | ModelType,
                     db_session: AsyncSession) -> ModelType:
        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.model_dump(
                exclude_unset=True
            )
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)
        return obj_current

    async def remove(self, *, uuid: UUID | str, session: AsyncSession) -> ModelType:
        query = select(self.model).where(self.model.uuid == uuid)
        response = await session.execute(query)
        obj = response.scalar_one()
        await session.delete(obj)
        await session.commit()
        return obj