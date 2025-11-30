from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional

from src.models.project import Project
from src.exceptions.repository_exceptions import NotFoundException

class ProjectRepository:
    """
    Repository layer for managing Project models in the database.
    Abstracts direct database interactions from the service layer.
    """
    def __init__(self, db_session: Session):
        self.session = db_session

    def add(self, name: str, description: Optional[str]) -> Project:
        """Adds a new Project to the database."""
        new_project = Project(
            name=name, 
            description=description
        )
        self.session.add(new_project)
        self.session.commit()
        self.session.refresh(new_project)
        return new_project

    def get_all(self) -> List[Project]:
        """Retrieves all projects."""
        return self.session.query(Project).all()

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Retrieves a single project by its ID."""
        return self.session.query(Project).filter(Project.id == project_id).first()

    # 💡 اصلاح: اضافه شدن name و description به امضا برای رفع TypeError
    def update(self, project: Project, name: str, description: Optional[str]) -> None:
        """Updates an existing project object and persists changes."""
        
        # 1. Update the attributes of the existing SQLAlchemy object
        project.name = name
        project.description = description
        
        # 2. Commit the changes to the database
        self.session.commit()
        
        # 3. Refresh the object to get any database-side updates (optional but good practice)
        self.session.refresh(project)
        # Note: We return None as the update is done in-place, and the service layer returns the object.

    def delete(self, project: Project) -> None:
        """Deletes a project object."""
        self.session.delete(project)
        self.session.commit()
