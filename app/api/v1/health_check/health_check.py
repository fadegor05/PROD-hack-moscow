from fastapi import APIRouter

health_check_router = APIRouter(prefix="/health_check", tags=["Health Check"])


@health_check_router.get(
    "",
    summary="Проверка работоспособности",
    description="Проверяет доступность и работоспособность сервиса"
)
async def get_health_check():
    return {"service": "healthy"}
