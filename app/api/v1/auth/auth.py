from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.core.decorators import dev_only
from app.core.exception import MultiLangHTTPExceptions
from app.core.jwt import create_access_token, get_current_user
from app.core.security import get_plain_hash
from app.database.database import get_async_session
from app.schemas.auth_schema import ILogin, IToken
from app.schemas.user_schema import IUserRegister

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register",
    status_code=201,
    responses={
        201: {
            "description": "Пользователь успешно зарегистрирован",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        409: {
            "description": "Пользователь уже существует",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "en": "User already exists",
                            "ru": "Пользователь уже существует",
                        }
                    }
                }
            },
        },
    },
    summary="Регистрация нового пользователя",
    description="Создает новую учетную запись пользователя и возвращает JWT токен доступа",
)
async def register(
        user_data: IUserRegister, session: AsyncSession = Depends(get_async_session)
) -> IToken:
    """
    Register a new user account.

    Creates a new user with the provided registration data and returns a JWT access token
    that can be used to authenticate future requests.

    Args:
        user_data: User registration data including:
            - phone: Unique phone number
            - password: User's password (will be hashed)
            - full_name: User's full name
        session: Database session

    Returns:
        JSON object containing:
            - access_token: JWT token for authentication
            - token_type: Type of token (always "bearer")

    Raises:
        409: If user with provided phone number already exists
    """
    try:
        user = await crud.user.register(obj_in=user_data, session=session)
    except:
        raise MultiLangHTTPExceptions.USER_ALREADY_EXISTS.to_exception()
    return IToken(access_token=create_access_token(user.uuid), token_type="bearer")


@auth_router.post(
    "/login",
    responses={
        200: {
            "description": "Успешная аутентификация",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        401: {
            "description": "Неверные учетные данные",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "en": "Invalid credentials",
                            "ru": "Неверные учетные данные",
                        }
                    }
                }
            },
        },
    },
    summary="Вход пользователя",
    description="Аутентифицирует учетные данные пользователя и возвращает JWT токен доступа",
)
async def login(login_data: ILogin, session: AsyncSession = Depends(get_async_session)) -> IToken:
    """
    Authenticate user and generate access token.

    Validates the provided credentials against stored user data and returns a JWT access token
    if authentication is successful.

    Args:
        login_data: User credentials including:
            - phone: User's registered phone number
            - password: User's password
        session: Database session

    Returns:
        JSON object containing:
            - access_token: JWT token for authentication
            - token_type: Type of token (always "bearer")

    Raises:
        401: If phone number doesn't exist or password is incorrect
    """
    user = await crud.user.get_by_phone(phone=login_data.phone, session=session)
    if not user:
        raise MultiLangHTTPExceptions.INVALID_CREDENTIALS.to_exception()

    hashed_password = await get_plain_hash(login_data.password)
    if hashed_password != user.hashed_password:
        raise MultiLangHTTPExceptions.INVALID_CREDENTIALS.to_exception()

    return IToken(access_token=create_access_token(user.uuid), token_type="bearer")


@auth_router.get(
    "/debug",
    summary="Отладочный эндпоинт (только для разработки)",
    description="Отладочный эндпоинт, доступный только в среде разработки. "
                "Этот эндпоинт не будет виден в продакшене.",
    include_in_schema=settings.ENV == "dev",
)
@dev_only()
async def debug_endpoint(current_user=Depends(get_current_user)):
    """
    Debug endpoint that's only available in development environment
    """
    return {
        "message": "This is a debug endpoint",
        "user": current_user,
        "environment": "development",
    }
