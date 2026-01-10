from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Better Auth / Frontend sync
    BETTER_AUTH_SECRET: Optional[str] = None

    PORT: int = 8000
    HOST: str = "0.0.0.0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
