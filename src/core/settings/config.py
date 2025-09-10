import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_URL: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 3 days = 3 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()