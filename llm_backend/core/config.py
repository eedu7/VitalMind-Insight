from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    OLLAMA_API_URL: str = Field("http://localhost:11343", description="Ollama Url")
    LLM_SECRET_TOKEN: str = Field("LLM_SECRET_TOKEN", description="Secret token for LLM API")
    GEMINI_API_KEY: str = Field(..., description="Google Gemini API Key")

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), extra="ignore")


settings = Settings()  # type: ignore
