from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

# Import Schemas, Services, Repositories, and Dependencies
from src.schemas import TaskCreate, TaskUpdate, TaskInDB
from src.repositories.task_repository import TaskRepository
from src.repositories.project_repository import ProjectRepository
from src.services.task_service import TaskService
from src.db.dependencies import get_db
from src.exceptions.repository_exceptions import NotFoundException
from src.models.task import TaskStatus

# Note: Tasks are nested under Projects
router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


# Dependency to initialize TaskService
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
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
        # Service handles validation (e.g., project_id existence)
        task = service.create_task(
            project_id=project_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline.isoformat() if task_data.deadline else None # Service expects ISO string or None
        )
        return task
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[TaskInDB])
def list_tasks_by_project(
    project_id: int, 
    service: TaskService = Depends(get_task_service)
):
    """Retrieve all tasks for a given project."""
    # Note: Service handles checking if the project exists
    tasks = service.list_tasks_by_project(project_id)
    if tasks is None: # Assuming service returns None/[] if project doesn't exist
         # We rely on the project existence check from the service layer
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project {project_id} not found.")
         
    return tasks


@router.put("/{task_id}", response_model=TaskInDB)
def update_task_in_project(
    project_id: int,
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Update an existing task."""
    try:
        # We need an update_task method in TaskService that handles both update and status change
        # Assuming the service method is implemented to take all necessary fields
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
def delete_task_in_project(
    project_id: int,
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Delete a task."""
    try:
        service.delete_task(project_id=project_id, task_id=task_id)
        # FastAPI returns 204 No Content for successful deletion by default
        return 
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
