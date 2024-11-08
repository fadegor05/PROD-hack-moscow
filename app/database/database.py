from app.core.config import PostgresSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

settings = PostgresSettings()
engine = create_async_engine(settings.postgres_url, echo=True)

async_session = async_sessionmaker(engine)


async def db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
