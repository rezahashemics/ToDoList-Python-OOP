# app/services/project_service.py
from app.repositories.project_repository import SqlAlchemyProjectRepository

class ProjectService:
    def __init__(self, repo=None):
        self.repo = repo or SqlAlchemyProjectRepository()

    def create_project(self, name: str, description: str | None = None):
        from app.models import Project
        project = Project(name=name, description=description)
        return self.repo.add(project)

    def list_projects(self):
        return self.repo.list()
