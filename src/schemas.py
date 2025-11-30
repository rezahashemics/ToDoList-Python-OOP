from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from src.models.task import TaskStatus # Import TaskStatus Enum

# --- Task Schemas ---

class TaskBase(BaseModel):
    """Base schema for common task fields."""
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskUpdate(TaskBase):
    """Schema for updating an existing task."""
    # Status is included here as it can be updated
    status: TaskStatus = TaskStatus.TODO

class TaskInDB(TaskBase):
    """Schema for returning Task data from the database."""
    id: int
    project_id: int
    status: TaskStatus
    closed_at: Optional[datetime] = None

    class Config:
        # Pydantic V2: Enables reading data from ORM objects (SQLAlchemy)
        from_attributes = True 
        # Note: use_enum_values = True is removed to fix the serialization error.
        
# --- Project Schemas ---

class ProjectBase(BaseModel):
    """Base schema for common project fields."""
    name: str = Field(..., max_length=50)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass

class ProjectInDB(ProjectBase):
    """Schema for returning Project data from the database."""
    id: int
    # Nested field: Includes all related tasks when querying a project
    tasks: List[TaskInDB] = [] 

    class Config:
        # Pydantic V2: Enables reading data from ORM objects (SQLAlchemy)
        from_attributes = True
        # Note: use_enum_values = True is removed.
