"""
app/schemas/task.py - Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class TaskBase(BaseModel):
    """Base task schema with common fields"""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(default="", max_length=2000, description="Task description")


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    
    @validator("title")
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()
    
    @validator("description")
    def validate_description(cls, v: Optional[str]) -> str:
        return v.strip() if v else ""


class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    completed: Optional[bool] = Field(None)
    
    @validator("title")
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Title cannot be empty or whitespace")
            return v.strip()
        return v
    
    @validator("description")
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v is not None else None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: str = Field(..., description="Unique task identifier")
    completed: bool = Field(..., description="Task completion status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")
    
    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class TaskList(BaseModel):
    """Schema for task list response"""
    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    completed: int = Field(..., description="Number of completed tasks")
    pending: int = Field(..., description="Number of pending tasks")


class TaskStats(BaseModel):
    """Schema for task statistics"""
    total_tasks: int = Field(..., description="Total number of tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    pending_tasks: int = Field(..., description="Number of pending tasks")
    completion_rate: float = Field(..., description="Completion rate as percentage")
    
    @validator("completion_rate")
    def round_completion_rate(cls, v: float) -> float:
        return round(v, 2)


class TaskToggleResponse(BaseModel):
    """Schema for task toggle response"""
    id: str = Field(..., description="Task identifier")
    completed: bool = Field(..., description="New completion status")
    message: str = Field(..., description="Success message")


class TaskDeleteResponse(BaseModel):
    """Schema for task deletion response"""
    id: str = Field(..., description="Deleted task identifier")
    message: str = Field(..., description="Success message")
