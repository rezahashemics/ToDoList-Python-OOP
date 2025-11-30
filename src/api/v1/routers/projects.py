from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import Schemas
from src.schemas import ProjectCreate, ProjectInDB

# Import Services and Repositories
from src.repositories.project_repository import ProjectRepository
from src.services.project_service import ProjectService
from src.db.dependencies import get_db
from src.exceptions.repository_exceptions import NotFoundException

router = APIRouter(prefix="/projects", tags=["Projects"])

# Dependency that creates and provides the ProjectService
def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency injection for ProjectService."""
    repo = ProjectRepository(db)
    return ProjectService(repo)


# ------------------ Endpoints ------------------

@router.post("/", response_model=ProjectInDB, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    """Create a new project."""
    try:
        project = service.create_project(
            name=project_data.name, 
            description=project_data.description
        )
        return project
    except ValueError as e:
        # Catches business logic errors (e.g., name validation)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ProjectInDB])
def list_projects(service: ProjectService = Depends(get_project_service)):
    """Retrieve a list of all projects."""
    return service.list_projects()


@router.get("/{project_id}", response_model=ProjectInDB)
def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    """Retrieve a single project by ID."""
    try:
        # Use repository directly for simple read operations where no business logic is needed
        project = service.repo.get_by_id(project_id) 
        if not project:
             raise NotFoundException
        return project
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project {project_id} not found")

@router.put("/{project_id}", response_model=ProjectInDB)
def update_project(
    project_id: int, 
    project_data: ProjectCreate, # Reusing ProjectCreate schema for input
    service: ProjectService = Depends(get_project_service)
):
    """Update an existing project."""
    try:
        # 💡 فراخوانی متد: این بخش اکنون با امضای تصحیح شده در Service مطابقت دارد
        updated_project = service.update_project(
            project_id=project_id,
            name=project_data.name,
            description=project_data.description
        )
        return updated_project
    except NotFoundException as e:
        # Project not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        # Business logic validation failed
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    service: ProjectService = Depends(get_project_service)
):
    """Delete a project."""
    try:
        service.delete_project(project_id)
        # Returns 204 No Content on successful deletion
        return 
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        # Catches optional business logic errors (e.g., cannot delete project with active tasks)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
