"""
app/core/exceptions.py - Custom exception classes
"""
from typing import Any, Dict, Optional


class TaskManagerException(Exception):
    """Base exception class for Task Manager application"""
    
    def __init__(
        self, 
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class TaskNotFoundError(TaskManagerException):
    """Exception raised when a task is not found"""
    
    def __init__(self, message: str = "Task not found"):
        super().__init__(message=message, error_code="TASK_NOT_FOUND")


class TaskValidationError(TaskManagerException):
    """Exception raised when task validation fails"""
    
    def __init__(self, message: str = "Task validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, error_code="TASK_VALIDATION_ERROR", details=details)


class DatabaseError(TaskManagerException):
    """Exception raised when database operation fails"""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message=message, error_code="DATABASE_ERROR")
