from src.repositories.project_repository import ProjectRepository
from src.exceptions.repository_exceptions import NotFoundException
from src.models.project import Project
from typing import List, Optional

class ProjectService:
    """
    Handles business logic and domain validation for Project operations.
    It acts as an intermediary between the API (or CLI) and the Repository.
    """
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def create_project(self, name: str, description: Optional[str]) -> Project:
        """Creates a new project after basic validation."""
        
        # Simple Validation: Name length (example business rule)
        if len(name.split()) > 10:
             raise ValueError("Project name must be <= 10 words.")
             
        return self.repo.add(name=name, description=description)

    def list_projects(self) -> List[Project]:
        """Retrieves all projects."""
        return self.repo.get_all()

    # 💡 اصلاح: اضافه شدن name: str و description: Optional[str] به امضای متد
    def update_project(self, project_id: int, name: str, description: Optional[str]) -> Project:
        """Updates an existing project by ID."""
        project = self.repo.get_by_id(project_id)
        
        if not project:
            raise NotFoundException(f"Project ID {project_id} not found.")

        # Simple Validation: Name length (example business rule)
        if len(name.split()) > 10:
             raise ValueError("Project name must be <= 10 words.")

        self.repo.update(
            project=project,
            name=name,
            description=description
        )
        return project

    def delete_project(self, project_id: int):
        """Deletes a project by ID."""
        project = self.repo.get_by_id(project_id)
        
        if not project:
            # Raising NotFoundException here ensures the API returns 404
            raise NotFoundException(f"Project ID {project_id} not found.")
            
        # Optional: Business logic check before deletion 
        # (e.g., prevent deletion if tasks are active)
        # if project.tasks:
        #     raise ValueError("Cannot delete project with active tasks.")

        self.repo.delete(project)
