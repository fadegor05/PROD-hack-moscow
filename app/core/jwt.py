from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.core.exception import MultiLangHTTPExceptions
from app.database.database import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id: UUID) -> str:
    """
    Create JWT access token for user
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expires_minutes)
    to_encode = {"exp": expire, "sub": str(user_id)}

    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get current authenticated user based on JWT token
    """
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise MultiLangHTTPExceptions.INVALID_CREDENTIALS.to_exception()
    except JWTError:
        raise MultiLangHTTPExceptions.INVALID_CREDENTIALS.to_exception()

    user = await crud.user.get(uuid=UUID(user_id), session=session)
    if user is None:
        raise MultiLangHTTPExceptions.INVALID_CREDENTIALS.to_exception()

    return user
