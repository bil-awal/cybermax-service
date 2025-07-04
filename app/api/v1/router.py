"""
app/api/v1/router.py - API router configuration
"""
from fastapi import APIRouter

from app.api.v1.endpoints import tasks

api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
