"""
app/utils/logger.py - Logging configuration
"""
import logging
import logging.handlers
from pathlib import Path

from app.core.config import get_settings

settings = get_settings()


def setup_logging():
    """Setup application logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.handlers.RotatingFileHandler(
                settings.LOG_FILE,
                maxBytes=10*1024*1024,
                backupCount=5
            )
        ]
    )
    
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
