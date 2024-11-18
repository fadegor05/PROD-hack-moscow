from contextlib import asynccontextmanager

from app.database.database import db
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db()
    yield
