import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Choose .env file based on Environment varialbe
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
print(ENVIRONMENT)

ENV_FILE = BASE_DIR / ".env.development" if ENVIRONMENT == "development" else ".env"
print(ENV_FILE)


class Settings(BaseSettings):
    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    PORT: int = 8080

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), extra="ignore")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()  # type: ignore
