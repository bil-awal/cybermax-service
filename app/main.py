"""
app/main.py - Main FastAPI application
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.database import create_tables, db_manager
from app.core.exceptions import TaskManagerException
from app.api.v1.router import api_router
from app.utils.logger import setup_logging

settings = get_settings()
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Task Manager API...")
    
    try:
        create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    if not db_manager.health_check():
        logger.error("Database health check failed")
        raise Exception("Database is not accessible")
    
    logger.info(f"Task Manager API started successfully on {settings.HOST}:{settings.PORT}")
    yield
    logger.info("Shutting down Task Manager API...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="A comprehensive task management API built with FastAPI",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        debug=settings.DEBUG,
        lifespan=lifespan
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()


@app.exception_handler(TaskManagerException)
async def task_manager_exception_handler(request: Request, exc: TaskManagerException):
    logger.error(f"TaskManager exception: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": exc.error_code, "type": "TaskManagerError"}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": exc.errors(), "type": "ValidationError"}
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "HTTPError"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error" if not settings.DEBUG else str(exc),
            "type": "InternalServerError"
        }
    )


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "api_prefix": "/api/v1"
    }


@app.get("/health", tags=["Health"])
def health_check():
    db_healthy = db_manager.health_check()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "timestamp": "2025-06-19T00:00:00Z",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": "connected" if db_healthy else "disconnected"
    }


@app.get("/info", tags=["Info"])
def get_app_info():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "database_type": "sqlite" if "sqlite" in settings.DATABASE_URL else "postgresql",
        "allowed_origins": settings.ALLOWED_ORIGINS,
        "log_level": settings.LOG_LEVEL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
