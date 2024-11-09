from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url="/openapi.json"
)

app.include_router(api_router)
