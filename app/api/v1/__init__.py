from fastapi import APIRouter

from .health_check.health_check import health_check_router

subrouters = (
    health_check_router,
)

v1_router = APIRouter()

for subrouter in subrouters:
    v1_router.include_router(subrouter)
