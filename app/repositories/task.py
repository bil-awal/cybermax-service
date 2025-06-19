"""
app/repositories/task.py - Task-specific repository
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    """Task repository with task-specific operations"""
    
    def __init__(self):
        super().__init__(Task)
    
    def get_by_title(self, db: Session, title: str) -> Optional[Task]:
        try:
            return db.query(Task).filter(Task.title == title).first()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def get_completed_tasks(self, db: Session) -> List[Task]:
        try:
            return db.query(Task).filter(Task.completed == True).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def get_pending_tasks(self, db: Session) -> List[Task]:
        try:
            return db.query(Task).filter(Task.completed == False).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def toggle_completion(self, db: Session, task_id: str) -> Optional[Task]:
        try:
            task = self.get(db, task_id)
            if task:
                task.toggle_completion()
                db.add(task)
                db.commit()
                db.refresh(task)
            return task
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def search_tasks(self, db: Session, query: str) -> List[Task]:
        try:
            search_term = f"%{query}%"
            return db.query(Task).filter(
                (Task.title.ilike(search_term)) | 
                (Task.description.ilike(search_term))
            ).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def get_task_stats(self, db: Session) -> dict:
        try:
            total = self.count(db)
            completed = db.query(Task).filter(Task.completed == True).count()
            pending = total - completed
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            return {
                "total_tasks": total,
                "completed_tasks": completed,
                "pending_tasks": pending,
                "completion_rate": completion_rate
            }
        except SQLAlchemyError as e:
            db.rollback()
            raise e


task_repository = TaskRepository()
