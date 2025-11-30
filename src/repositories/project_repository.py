from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.project import Project

# Note: We don't inherit from BaseRepository for simplicity here, 
# but in a production environment, an abstract interface is ideal.

class ProjectRepository:
    """Handles direct database operations for Project entities."""
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str = "") -> Project:
        new_project = Project(name=name, description=description)
        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project) 
        return new_project

    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.get(Project, project_id)

    def get_all(self) -> List[Project]:
        stmt = select(Project).order_by(Project.id)
        return self.db.scalars(stmt).all()

    def update(self, project: Project, new_name: str, new_desc: str):
        # Validation that 'project' object is valid should be done in the Service layer
        project.name = new_name
        project.description = new_desc
        self.db.commit()

    def delete(self, project: Project):
        # Cascade delete handled by relationship in models
        self.db.delete(project)
        self.db.commit()
