from fastapi import FastAPI, APIRouter

from app.api import api_router


class Server:
    app: FastAPI

    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.register_router(api_router)

    def get_app(self) -> FastAPI:
        return self.app

    def register_router(self, router: APIRouter) -> None:
        self.app.include_router(router)
