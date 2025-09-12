from pathlib import Path
from typing import List, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


ENV_FILE = BASE_DIR / ".env"

TYPE_COOKIE_SAMESITE = Literal["strict", "lax", "none"]


class Settings(BaseSettings):
    # Database
    DB_USER: str = "myuser"
    DB_PASSWORD: str = "mypassword"
    DB_NAME: str = "mydb"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    # Test
    TEST_DB_USER: str = "myuser"
    TEST_DB_PASSWORD: str = "mypassword"
    TEST_DB_NAME: str = "mydb"
    TEST_DB_HOST: str = "localhost"
    TEST_DB_PORT: int = 5433

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Test Redis
    TEST_REDIS_HOST: str = "localhost"
    TEST_REDIS_PORT: int = 6380

    # Cookie
    COOKIE_SECURE: bool = True
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: TYPE_COOKIE_SAMESITE = "lax"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:8080"

    # App
    PORT: int = 8080

    # JWT
    JWT_SECRET_KEY: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE_MINUTES: int = 60 * 24
    JWT_REFRESH_EXPIRE_MINUTES: int = 60 * 24 * 7

    # LLM
    LLM_SECRET_TOKEN: str = Field("LLM_SECRET_TOKEN", description="Secret token for LLM API")

    # Environment
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), extra="ignore")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def TEST_REDIS_URL(self) -> str:
        return f"redis://{self.TEST_REDIS_HOST}:{self.TEST_REDIS_PORT}"

    @property
    def GET_ALLOWED_ORIGINS(self) -> List[str]:
        return self.ALLOWED_ORIGINS.split(",")


settings = Settings()  # type: ignore
