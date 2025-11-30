from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

# Import Schemas, Services, Repositories, and Dependencies
from src.schemas import TaskCreate, TaskUpdate, TaskInDB
from src.repositories.task_repository import TaskRepository
from src.repositories.project_repository import ProjectRepository
from src.services.task_service import TaskService
from src.db.dependencies import get_db
from src.exceptions.repository_exceptions import NotFoundException

# Tasks are nested under Projects, hence the dynamic path prefix
router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


# Dependency to initialize TaskService
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency injection for TaskService."""
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    return TaskService(task_repo, project_repo)


# ------------------ Endpoints ------------------

@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
def create_task_for_project(
    project_id: int, 
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    """Create a new task within a specific project."""
    try:
        # Note: We pass deadline as string, service handles parsing
        task = service.create_task(
            project_id=project_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline.isoformat() if task_data.deadline else None
        )
        return task
    except NotFoundException as e:
        # Project not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        # Validation or date parsing error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[TaskInDB])
def list_tasks_by_project(
    project_id: int, 
    service: TaskService = Depends(get_task_service)
):
    """Retrieve all tasks for a given project."""
    try:
        # Service throws 404 if project is not found
        return service.list_tasks_by_project(project_id)
    except NotFoundException as e:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{task_id}", response_model=TaskInDB)
def update_task_in_project(
    project_id: int,
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Update an existing task, including status change."""
    try:
        # Note: We pass deadline as string, service handles parsing
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
        # Project or Task not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        # Validation or date parsing error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_in_project(
    project_id: int,
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Delete a task."""
    try:
        service.delete_task(project_id=project_id, task_id=task_id)
        # 204 No Content is returned on successful deletion
        return 
    except NotFoundException as e:
        # Task not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
