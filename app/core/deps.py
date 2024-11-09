from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import JWTSettings
from app.database.database import get_async_session
from app.models.user_model import User

settings = JWTSettings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Dependency to get the current authenticated user from a JWT token.

    This dependency:
    1. Extracts and validates the JWT token from the Authorization header
    2. Decodes the token to get the user UUID
    3. Retrieves the corresponding user from the database

    Args:
        token: JWT token extracted from the Authorization header
        session: Database session for querying user data

    Returns:
        User: The authenticated user model if token is valid

    Raises:
        HTTPException: 401 Unauthorized if:
            - Token is invalid or expired
            - Token payload doesn't contain user UUID
            - User not found in database

    Usage:
        ```python
        @router.get("/protected")
        async def protected_route(
            current_user: Annotated[User, Depends(get_current_user)]
        ):
            return {"msg": f"Hello {current_user.full_name}"}
        ```
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_uuid: str = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud.user.get(uuid=user_uuid, session=session)
    if user is None:
        raise credentials_exception

    return user
