from pathlib import Path
from typing import List, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


ENV_FILE = BASE_DIR / ".env"

TYPE_COOKIE_SAMESITE = Literal["strict", "lax", "none"]


class Settings(BaseSettings):
    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    # Test
    TEST_DB_USER: str
    TEST_PASSWORD: str
    TEST_DB_NAME: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

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

    # Environment
    ENVIRONMENT: str

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), extra="ignore")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def GET_ALLOWED_ORIGINS(self) -> List[str]:
        return self.ALLOWED_ORIGINS.split(",")


settings = Settings()  # type: ignore
