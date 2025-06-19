import os
from typing import List

try:
    from pydantic import BaseSettings, validator
except ImportError:
    from pydantic_settings import BaseSettings
    from pydantic import validator


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    APP_NAME: str = "Task Manager API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./task_manager.db"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # Security
    SECRET_KEY: str = "development-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v: str, values: dict) -> str:
        if values.get("ENVIRONMENT") == "production" and v == "development-secret-key":
            raise ValueError("SECRET_KEY must be set in production")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = ""  # no prefix
        # Allow parsing booleans from strings like "true"/"false"
        # Pydantic handles this by default


# Instantiate settings once
settings = Settings()


def get_settings() -> Settings:
    return settings
