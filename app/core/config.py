from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    CASES_TABLE: str
    USERS_TABLE: str
    SECRET_KEY: str
    APP_ENV: str = "production"

    class Config:
        env_file = str(BASE_DIR / ".env")


settings = Settings()
