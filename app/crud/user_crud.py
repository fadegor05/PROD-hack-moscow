from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_plain_hash
from app.crud.base_crud import BaseCRUD
from app.models.user_model import User
from app.schemas.user_schema import IUserCreate, IUserUpdate


class UserCRUD(BaseCRUD[User, IUserCreate, IUserUpdate]):
    async def create(self, *, obj_in: IUserCreate, session: AsyncSession) -> User:
        obj_in.hashed_password = await get_plain_hash(obj_in.password)
        return await super().create(obj_in=obj_in, session=session)


user = UserCRUD(User)
