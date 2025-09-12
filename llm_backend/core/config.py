from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    OLLAMA_API_URL: str = "http://localhost:11343"
    LLM_SECRET_TOKEN: str = Field("LLM_SECRET_TOKEN", description="Secret token for LLM API")

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), extra="ignore")


settings = Settings()
