"""
app/models/task.py - Task SQLAlchemy model
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Task(Base):
    """Task model representing a task in the database"""
    __tablename__ = "tasks"
    
    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True, default="")
    completed = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"{status} {self.title}"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def toggle_completion(self) -> bool:
        self.completed = not self.completed
        return self.completed
