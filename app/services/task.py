"""
app/services/task.py - Task service layer containing business logic
"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.models.task import Task
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskList, TaskStats,
    TaskToggleResponse, TaskDeleteResponse
)
from app.repositories.task import task_repository
from app.core.exceptions import TaskNotFoundError, TaskValidationError, DatabaseError

logger = logging.getLogger(__name__)


class TaskService:
    """Task service containing business logic for task operations"""
    
    def __init__(self):
        self.repository = task_repository
    
    def get_all_tasks(self, db: Session, skip: int = 0, limit: int = 100) -> TaskList:
        try:
            tasks = self.repository.get_multi(db, skip=skip, limit=limit)
            stats = self.repository.get_task_stats(db)
            
            return TaskList(
                tasks=[TaskResponse.from_orm(task) for task in tasks],
                total=stats["total_tasks"],
                completed=stats["completed_tasks"],
                pending=stats["pending_tasks"]
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching tasks: {e}")
            raise DatabaseError("Failed to fetch tasks")
    
    def get_task_by_id(self, db: Session, task_id: str) -> TaskResponse:
        try:
            task = self.repository.get(db, task_id)
            if not task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            return TaskResponse.from_orm(task)
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching task {task_id}: {e}")
            raise DatabaseError(f"Failed to fetch task {task_id}")
    
    def create_task(self, db: Session, task_data: TaskCreate) -> TaskResponse:
        try:
            task = self.repository.create(db, obj_in=task_data)
            logger.info(f"Created new task: {task.id} - {task.title}")
            return TaskResponse.from_orm(task)
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating task: {e}")
            raise DatabaseError("Failed to create task")
    
    def update_task(self, db: Session, task_id: str, task_data: TaskUpdate) -> TaskResponse:
        try:
            existing_task = self.repository.get(db, task_id)
            if not existing_task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            updated_task = self.repository.update(db, db_obj=existing_task, obj_in=task_data)
            logger.info(f"Updated task: {task_id} - {updated_task.title}")
            return TaskResponse.from_orm(updated_task)
        except SQLAlchemyError as e:
            logger.error(f"Database error while updating task {task_id}: {e}")
            raise DatabaseError(f"Failed to update task {task_id}")
    
    def toggle_task_completion(self, db: Session, task_id: str) -> TaskToggleResponse:
        try:
            task = self.repository.toggle_completion(db, task_id)
            if not task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            status_text = "completed" if task.completed else "marked as pending"
            logger.info(f"Task {task_id} {status_text}")
            
            return TaskToggleResponse(
                id=task.id,
                completed=task.completed,
                message=f"Task {status_text} successfully"
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error while toggling task {task_id}: {e}")
            raise DatabaseError(f"Failed to toggle task {task_id}")
    
    def delete_task(self, db: Session, task_id: str) -> TaskDeleteResponse:
        try:
            deleted_task = self.repository.delete(db, id=task_id)
            if not deleted_task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            logger.info(f"Deleted task: {task_id} - {deleted_task.title}")
            return TaskDeleteResponse(id=task_id, message="Task deleted successfully")
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting task {task_id}: {e}")
            raise DatabaseError(f"Failed to delete task {task_id}")
    
    def search_tasks(self, db: Session, query: str) -> List[TaskResponse]:
        try:
            if not query or len(query.strip()) < 2:
                raise TaskValidationError("Search query must be at least 2 characters long")
            
            tasks = self.repository.search_tasks(db, query.strip())
            logger.info(f"Search for '{query}' returned {len(tasks)} results")
            return [TaskResponse.from_orm(task) for task in tasks]
        except SQLAlchemyError as e:
            logger.error(f"Database error while searching tasks: {e}")
            raise DatabaseError("Failed to search tasks")
    
    def get_task_statistics(self, db: Session) -> TaskStats:
        try:
            stats = self.repository.get_task_stats(db)
            return TaskStats(**stats)
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching task statistics: {e}")
            raise DatabaseError("Failed to fetch task statistics")
    
    def get_completed_tasks(self, db: Session) -> List[TaskResponse]:
        try:
            tasks = self.repository.get_completed_tasks(db)
            return [TaskResponse.from_orm(task) for task in tasks]
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching completed tasks: {e}")
            raise DatabaseError("Failed to fetch completed tasks")
    
    def get_pending_tasks(self, db: Session) -> List[TaskResponse]:
        try:
            tasks = self.repository.get_pending_tasks(db)
            return [TaskResponse.from_orm(task) for task in tasks]
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching pending tasks: {e}")
            raise DatabaseError("Failed to fetch pending tasks")


task_service = TaskService()
