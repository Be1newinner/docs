from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # our app configuration
    DATABASE_URL: str = Field(default=..., validation_alias="DATABASE_URL")
    SECRET_KEY: str = Field(default=..., validation_alias="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application Settings
    APP_NAME: str = "FAANG Auth Service"
    API_V1_STR: str = "/api/v1"

settings = Settings()
