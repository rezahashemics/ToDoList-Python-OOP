from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import Schemas, Models, Services
from src.schemas import TaskCreate, TaskUpdate, TaskInDB
from src.models.task import TaskStatus
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService
from src.db.dependencies import get_db
from src.exceptions.repository_exceptions import NotFoundException

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency injection for TaskService."""
    repo = TaskRepository(db)
    return TaskService(repo)

# ------------------ Endpoints ------------------

@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
def create_task_for_project(
    project_id: int,
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    """Create a new task within a specified project."""
    try:
        task = service.create_task(
            project_id=project_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline.isoformat() if task_data.deadline else None 
        )
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    # Note: If Project ID is invalid (FK violation), SQLAlchemy usually raises IntegrityError 
    # which results in a 500, unless specifically caught and handled.

@router.get("/{task_id}", response_model=TaskInDB)
def get_task_for_project(
    project_id: int, 
    task_id: int, 
    service: TaskService = Depends(get_task_service)
):
    """Retrieve a single task by its ID."""
    try:
        task = service.get_task_by_id(project_id, task_id)
        return task
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# 💡 بخش به‌روزرسانی (PUT)
@router.put("/{task_id}", response_model=TaskInDB)
def update_task_for_project(
    project_id: int, 
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Update an existing task."""
    try:
        updated_task = service.update_task(
            project_id=project_id,
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline.isoformat() if task_data.deadline else None,
            status=task_data.status
        )
        return updated_task
    except NotFoundException as e:
        # 💡 NotFoundException را از Service دریافت کرده و 404 برمی‌گرداند.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_for_project(
    project_id: int, 
    task_id: int, 
    service: TaskService = Depends(get_task_service)
):
    """Delete a task."""
    try:
        service.delete_task(project_id, task_id)
        return 
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
