from pydantic import computed_field
from pydantic_settings import BaseSettings
from functools import lru_cache


class JWTSettings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60 * 24  # 1 day

    class Config:
        extra = "allow"
        env_file = ".env"


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
        env_file = ".env"


class ParserSettings(BaseSettings):
    proverkacheka_token: str

    class Config:
        extra = "allow"
        env_file = ".env"


class GeminiSettings(BaseSettings):
    gemini_api_key: str | None = None  # Make this field optional

    class Config:
        extra = "allow"
        env_file = ".env"


class Settings(BaseSettings):
    # Basic settings
    ENV: str = "prod"
    PROJECT_NAME: str = "FastAPI App"

    # Backend settings
    backend_port: str

    # Database settings
    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    # Parser settings
    proverkacheka_token: str

    # Gemini settings
    gemini_api_key: str | None = None  # Make this field optional

    # JWT settings
    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_minutes: int

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
