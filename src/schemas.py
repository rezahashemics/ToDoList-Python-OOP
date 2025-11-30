from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from src.models.task import TaskStatus # Import TaskStatus Enum

# --- Base Schemas ---

class TaskStatusSchema(BaseModel):
    """Schema for TaskStatus Enum used in Pydantic."""
    # This ensures Pydantic handles the enum correctly
    __root__: TaskStatus 

# --- Task Schemas ---

class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    # project_id will be captured from the URL path in the router
    pass

class TaskUpdate(TaskBase):
    status: TaskStatus = TaskStatus.TODO

class TaskInDB(TaskBase):
    """Schema for returning Task data."""
    id: int
    project_id: int
    status: TaskStatus
    closed_at: Optional[datetime] = None

    class Config:
        # Allows Pydantic to read ORM objects (Task model)
        orm_mode = True 
        use_enum_values = True 
        
# --- Project Schemas ---

class ProjectBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectInDB(ProjectBase):
    """Schema for returning Project data."""
    id: int
    # Nested field to include related tasks in project response
    tasks: List[TaskInDB] = [] 

    class Config:
        orm_mode = True
