import pytest
import os
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

os.environ["ENVIRONMENT"] = "testing"
os.environ["DATABASE_URL"] = "sqlite:///./test_task_manager.db"
os.environ["DEBUG"] = "True"

from app.main import app
from app.core.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_task_manager.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    
    import os
    if os.path.exists("test_task_manager.db"):
        os.remove("test_task_manager.db")


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_task_data():
    return {"title": "Test Task", "description": "This is a test task"}


@pytest.fixture
def sample_task(db_session: Session, sample_task_data):
    from app.services.task import task_service
    from app.schemas.task import TaskCreate
    
    task_data = TaskCreate(**sample_task_data)
    task = task_service.create_task(db_session, task_data)
    return task
