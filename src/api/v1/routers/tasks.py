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


# 💡 اضافه شدن این متد حیاتی برای GET /v1/projects/{project_id}/tasks/
@router.get("/", response_model=List[TaskInDB]) 
def list_tasks_for_project(
    project_id: int, 
    service: TaskService = Depends(get_task_service)
):
    """Retrieve a list of all tasks for a specific project."""
    # Note: If list_tasks_by_project logic ensures project existence, 
    # we might need to add ProjectService dependency here to check for 404 on project_id.
    # For now, relying on list_tasks_by_project to return an empty list if project exists 
    # but has no tasks, or letting an IntegrityError pass as 500 if project doesn't exist.
    return service.list_tasks_by_project(project_id)


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
