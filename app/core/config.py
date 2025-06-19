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
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./task_manager.db"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "https://cybermax-web.vercel.app"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # Security
    SECRET_KEY: str = "development-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Heroku-specific overrides
        if os.getenv('DYNO'):  # Heroku environment detected
            self.ENVIRONMENT = "production"
            self.DEBUG = False
            self.RELOAD = False
            
            # Use Heroku's assigned port
            if os.getenv('PORT'):
                self.PORT = int(os.getenv('PORT'))
            
            # Use DATABASE_URL from Heroku if available
            if os.getenv('DATABASE_URL'):
                db_url = os.getenv('DATABASE_URL')
                # Convert postgres:// to postgresql:// if needed
                if db_url.startswith('postgres://'):
                    db_url = db_url.replace('postgres://', 'postgresql://', 1)
                self.DATABASE_URL = db_url
            
            # Set secret key from environment
            if os.getenv('SECRET_KEY'):
                self.SECRET_KEY = os.getenv('SECRET_KEY')
                
        # Local development overrides
        else:
            # Load from .env file for local development
            if os.path.exists('.env'):
                from dotenv import load_dotenv
                load_dotenv()
            
            self.DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
            self.RELOAD = os.getenv('RELOAD', 'true').lower() == 'true'
            self.DATABASE_URL = os.getenv('DATABASE_URL', self.DATABASE_URL)
            self.HOST = os.getenv('HOST', self.HOST)
            if os.getenv('PORT'):
                self.PORT = int(os.getenv('PORT'))
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v: str, values: dict) -> str:
        env = values.get("ENVIRONMENT", "development")
        if env == "production" and v in ("change-this-in-production", "development-secret-key"):
            # Try to get from environment
            secret = os.getenv('SECRET_KEY')
            if secret:
                return secret
            raise ValueError("SECRET_KEY must be set in production environment")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

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
