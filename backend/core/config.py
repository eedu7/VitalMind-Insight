from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
