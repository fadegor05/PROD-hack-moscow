from fastapi import APIRouter

from .health_check.health_check import health_check_router
from .receipt.receipt import receipt_router
from .users.users import users_router

subrouters = (
    health_check_router,
    users_router,
    receipt_router,
)

v1_router = APIRouter()

for subrouter in subrouters:
    v1_router.include_router(subrouter)
