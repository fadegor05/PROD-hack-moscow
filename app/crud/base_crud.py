from typing import TypeVar, Generic, List, Any
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.common_schema import IOrderEnum

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


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
                     session: AsyncSession) -> ModelType:
        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.model_dump(
                exclude_unset=True
            )
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        session.add(obj_current)
        await session.commit()
        await session.refresh(obj_current)
        return obj_current

    async def remove(self, *, uuid: UUID | str, session: AsyncSession) -> ModelType | None:
        query = select(self.model).where(self.model.uuid == uuid)
        response = await session.execute(query)
        obj = response.scalar_one_or_none()
        await session.delete(obj)
        await session.commit()
        return obj

    async def get_multi_ordered(self, *, skip: int = 0,
                                limit: int = 100, order_by: str, order: IOrderEnum = IOrderEnum.ascendent,
                                session: AsyncSession) -> List[ModelType]:
        columns = self.model.__table__.columns

        if order_by is None or order_by not in columns:
            order_by = "uuid"

        if order == IOrderEnum.ascendent:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by].asc())
            )
        else:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by].desc())
            )

        response = await session.execute(query)
        return response.scalars().all()

    async def get_with_uuid_columns(self, *, uuid: UUID | str, session: AsyncSession,
                                    columns: List[str], read_interface: ReadSchemaType) -> ReadSchemaType | None:
        obj = await self.get(uuid=uuid, session=session)
        if obj is None:
            return None
        extended_data = obj.model_dump()

        for column in columns:
            if hasattr(obj, column):
                attr_value = getattr(obj, column)

                if isinstance(attr_value, list) and all(hasattr(item, 'uuid') for item in attr_value):
                    extended_data[f"{column}_uuid"] = [item.uuid for item in attr_value]
                elif hasattr(attr_value, 'uuid'):
                    extended_data[f"{column}_uuid"] = attr_value.uuid
                else:
                    extended_data[column] = attr_value
        return read_interface.model_validate(extended_data)

    async def get_multi_ordered_with_uuid_columns(
            self, *,
            skip: int = 0,
            limit: int = 100,
            order_by: str,
            order: IOrderEnum = IOrderEnum.ascendent,
            session: AsyncSession,
            columns: List[str],
            read_interface: type[ReadSchemaType]
    ) -> List[ReadSchemaType]:
        columns_mapping = self.model.__table__.columns

        if order_by is None or order_by not in columns_mapping:
            order_by = "uuid"

        query = (
            select(self.model)
            .offset(skip)
            .limit(limit)
            .order_by(
                columns_mapping[order_by].asc() if order == IOrderEnum.ascendent else columns_mapping[order_by].desc())
        )

        response = await session.execute(query)
        objs = response.scalars().all()

        extended_objs = []

        for obj in objs:
            extended_data = obj.dict()

            for column in columns:
                if hasattr(obj, column):
                    attr_value = getattr(obj, column)

                    if isinstance(attr_value, list) and all(hasattr(item, 'uuid') for item in attr_value):
                        extended_data[f"{column}_uuid"] = [item.uuid for item in attr_value]
                    elif hasattr(attr_value, 'uuid'):
                        extended_data[f"{column}_uuid"] = attr_value.uuid
                    else:
                        extended_data[column] = attr_value

            extended_objs.append(read_interface(**extended_data))

        return extended_objs
