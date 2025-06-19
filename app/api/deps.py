"""
app/api/deps.py - API dependencies
"""
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import get_settings, Settings


def get_current_settings() -> Settings:
    return get_settings()


def get_database_session() -> Generator[Session, None, None]:
    yield from get_db()
