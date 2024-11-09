from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_plain_hash
from app.crud.base_crud import BaseCRUD
from app.models.user_model import User
from app.schemas.user_schema import IUserCreate, IUserUpdate


class UserCRUD(BaseCRUD[User, IUserCreate, IUserUpdate]):
    async def register(self, *, obj_in: IUserCreate, session: AsyncSession) -> User:
        hashed_password = await get_plain_hash(obj_in.password)
        user_data = obj_in.model_dump(exclude={"password"})
        db_user = self.model(**user_data, hashed_password=hashed_password)
        return await super().create(obj_in=db_user, session=session)

    async def get_by_phone(self, *, phone: str, session: AsyncSession) -> User | None:
        statement = select(self.model).where(self.model.phone == phone)
        response = await session.execute(statement)
        return response.scalar_one_or_none()


user = UserCRUD(User)
