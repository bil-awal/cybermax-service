"""
app/api/v1/endpoints/tasks.py - Task endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_database_session
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskList, TaskStats,
    TaskToggleResponse, TaskDeleteResponse
)
from app.services.task import task_service
from app.core.exceptions import TaskNotFoundError, TaskValidationError, DatabaseError

router = APIRouter()


@router.get("/", response_model=TaskList, summary="Get all tasks")
def get_all_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    db: Session = Depends(get_database_session)
) -> TaskList:
    try:
        return task_service.get_all_tasks(db, skip=skip, limit=limit)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Create a new task")
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_database_session)
) -> TaskResponse:
    try:
        return task_service.create_task(db, task_data)
    except TaskValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse, summary="Get a specific task")
def get_task(
    task_id: str,
    db: Session = Depends(get_database_session)
) -> TaskResponse:
    try:
        return task_service.get_task_by_id(db, task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse, summary="Update a task")
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_database_session)
) -> TaskResponse:
    try:
        return task_service.update_task(db, task_id, task_data)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaskValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{task_id}/toggle", response_model=TaskToggleResponse, summary="Toggle task completion")
def toggle_task_completion(
    task_id: str,
    db: Session = Depends(get_database_session)
) -> TaskToggleResponse:
    try:
        return task_service.toggle_task_completion(db, task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{task_id}", response_model=TaskDeleteResponse, summary="Delete a task")
def delete_task(
    task_id: str,
    db: Session = Depends(get_database_session)
) -> TaskDeleteResponse:
    try:
        return task_service.delete_task(db, task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/search/", response_model=List[TaskResponse], summary="Search tasks")
def search_tasks(
    q: str = Query(..., min_length=2, description="Search query"),
    db: Session = Depends(get_database_session)
) -> List[TaskResponse]:
    try:
        return task_service.search_tasks(db, q)
    except TaskValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/stats/", response_model=TaskStats, summary="Get task statistics")
def get_task_statistics(
    db: Session = Depends(get_database_session)
) -> TaskStats:
    try:
        return task_service.get_task_statistics(db)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/completed/", response_model=List[TaskResponse], summary="Get completed tasks")
def get_completed_tasks(
    db: Session = Depends(get_database_session)
) -> List[TaskResponse]:
    try:
        return task_service.get_completed_tasks(db)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/pending/", response_model=List[TaskResponse], summary="Get pending tasks")
def get_pending_tasks(
    db: Session = Depends(get_database_session)
) -> List[TaskResponse]:
    try:
        return task_service.get_pending_tasks(db)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/seed", summary="Seed sample data")
def seed_sample_data(
    db: Session = Depends(get_database_session)
) -> dict:
    sample_tasks = [
        TaskCreate(title="Learn FastAPI", description="Study FastAPI framework and build REST APIs"),
        TaskCreate(title="Build Frontend", description="Create React TypeScript frontend"),
        TaskCreate(title="Deploy to Vercel", description="Setup deployment pipeline"),
        TaskCreate(title="Write Tests", description="Add comprehensive test coverage"),
        TaskCreate(title="Documentation", description="Write API documentation and README"),
    ]
    
    created_tasks = []
    try:
        for task_data in sample_tasks:
            task = task_service.create_task(db, task_data)
            created_tasks.append(task)
        
        return {
            "message": f"Successfully created {len(created_tasks)} sample tasks",
            "tasks": created_tasks
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create sample data: {str(e)}"
        )
