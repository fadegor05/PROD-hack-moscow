from functools import wraps
from fastapi import HTTPException
from app.core.config import settings


def dev_only():
    def decorator(func):
        if hasattr(func, "__api_route__"):
            if settings.ENV != "dev":
                func.__api_route__.include_in_schema = False

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if settings.ENV != "dev":
                raise HTTPException(
                    status_code=403,
                    detail="This endpoint is only available in development environment",
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
