from pydantic import computed_field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    @computed_field
    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@postgres:{self.postgres_port}/{self.postgres_db}"

    class Config:
        extra = "allow"
