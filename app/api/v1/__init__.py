from fastapi import APIRouter

from .auth.auth import auth_router
from .events.events import events_router
from .health_check.health_check import health_check_router
from .receipts.receipts import receipts_router
from .users.users import users_router

subrouters = (
    health_check_router,
    users_router,
    receipts_router,
    auth_router,
    events_router,
)

v1_router = APIRouter(prefix="/v1")

for subrouter in subrouters:
    v1_router.include_router(subrouter)
