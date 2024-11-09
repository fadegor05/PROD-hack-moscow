from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.core.server import Server
from .core.config import settings
from .models import *


def create_app(_=None) -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
    return Server(app).get_app()
