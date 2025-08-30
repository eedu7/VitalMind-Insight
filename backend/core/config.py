from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

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


settings = Settings()  # type: ignore
