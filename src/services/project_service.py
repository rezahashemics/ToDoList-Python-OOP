from typing import List
from src.repositories.project_repository import ProjectRepository
from src.models.project import Project
from src.exceptions.repository_exceptions import NotFoundException # Assuming you create this

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def create_project(self, name: str, description: str = "") -> Project:
        # Business Logic: Validation (e.g., word count validation should be here)
        if len(name.split()) > 30:
            raise ValueError("Project name must be <= 30 words")
        
        return self.repo.create(name=name, description=description)

    def list_projects(self) -> List[Project]:
        return self.repo.get_all()

    def update_project(self, project_id: int, new_name: str, new_desc: str):
        project = self.repo.get_by_id(project_id)
        if not project:
            raise NotFoundException(f"Project ID {project_id} not found.")

        # Business Logic: Validation
        if len(new_name.split()) > 30:
            raise ValueError("Project name must be <= 30 words")

        self.repo.update(project, new_name, new_desc)

    def delete_project(self, project_id: int):
        project = self.repo.get_by_id(project_id)
        if not project:
            raise NotFoundException(f"Project ID {project_id} not found.")
        
        self.repo.delete(project)
