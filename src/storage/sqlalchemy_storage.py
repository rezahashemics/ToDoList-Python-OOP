from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from src.core.models import Project, Task, TaskStatus
# Assuming you have a base interface in src.storage.base or similar 
# For simplicity, we just implement the methods directly

class SQLAlchemyStorage:
    def __init__(self, db: Session):
        # We receive a SQLAlchemy Session object to interact with the database
        self.db = db

    # --- Project Operations ---

    def create_project(self, name: str, description: str = "") -> Project:
        # Create a new Project instance (not yet committed to DB)
        new_project = Project(name=name, description=description)
        # Add to session and commit
        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project) # Get the generated ID
        return new_project

    def get_project(self, project_id: int) -> Optional[Project]:
        # Query the Project by ID
        return self.db.get(Project, project_id)

    def get_all_projects(self) -> List[Project]:
        # Select all projects
        stmt = select(Project).order_by(Project.id)
        return self.db.execute(stmt).scalars().all()

    def update_project(self, project_id: int, new_name: str, new_desc: str):
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found.")
        
        project.name = new_name
        project.description = new_desc
        self.db.commit() # Commit changes

    def delete_project(self, project_id: int):
        # Cascading delete is handled by the relationship in models.py
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found.")

        self.db.delete(project)
        self.db.commit()

    # --- Task Operations ---
    
    # Helper to parse deadline string to datetime
    def _parse_deadline(self, deadline: Optional[str]) -> Optional[datetime]:
        if not deadline:
            return None
        try:
            return datetime.fromisoformat(deadline)
        except ValueError:
            raise ValueError("Invalid deadline format. Use YYYY-MM-DDTHH:MM:SS")


    def create_task(
        self,
        project_id: int,
        title: str,
        description: str,
        status: str, # status is passed as a string from CLI
        deadline: Optional[str],
    ) -> Task:
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found for task creation.")

        task_status = TaskStatus(status) # Convert string to Enum
        dt_deadline = self._parse_deadline(deadline)
        
        new_task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=task_status,
            deadline=dt_deadline,
        )

        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def get_tasks_for_project(self, project_id: int) -> List[Task]:
        # Select all tasks for a specific project ID
        stmt = select(Task).where(Task.project_id == project_id)
        return self.db.execute(stmt).scalars().all()

    def update_task_status(self, project_id: int, task_id: int, new_status: str):
        # We need to find the specific task
        stmt = select(Task).where(Task.project_id == project_id, Task.id == task_id)
        task = self.db.execute(stmt).scalar_one_or_none()

        if not task:
            raise ValueError(f"Task ID {task_id} not found in Project ID {project_id}.")
        
        task.status = TaskStatus(new_status)
        self.db.commit()

    def update_task(
        self,
        project_id: int,
        task_id: int,
        title: str,
        description: str,
        deadline: Optional[str],
        status: str,
    ):
        stmt = select(Task).where(Task.project_id == project_id, Task.id == task_id)
        task = self.db.execute(stmt).scalar_one_or_none()

        if not task:
            raise ValueError(f"Task ID {task_id} not found in Project ID {project_id}.")
        
        task.title = title
        task.description = description
        task.deadline = self._parse_deadline(deadline)
        task.status = TaskStatus(status)
        
        self.db.commit()
        
    def delete_task(self, project_id: int, task_id: int):
        # Use a delete statement for efficiency
        stmt = delete(Task).where(Task.project_id == project_id, Task.id == task_id)
        result = self.db.execute(stmt)
        if result.rowcount == 0:
            raise ValueError(f"Task ID {task_id} not found in Project ID {project_id}.")
        self.db.commit()
