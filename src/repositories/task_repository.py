from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.models.task import Task, TaskStatus
from src.models.project import Project
from src.exceptions.repository_exceptions import NotFoundException

class TaskRepository:
    """
    Repository layer for managing Task models in the database.
    """
    def __init__(self, db_session: Session):
        self.session = db_session

    # 💡 این متد add باید وجود داشته باشد
    def add(self, project_id: int, title: str, description: Optional[str], deadline: Optional[datetime]) -> Task:
        """Adds a new Task to the database."""
        
        # Check if the project exists (optional but good for early failure)
        # Note: We commented this out in previous examples, but keeping it as a check point
        # if not self.session.query(Project).filter(Project.id == project_id).first():
        #     # In the service layer, we also check this, so commenting this out for repository purity
        #     # raise NotFoundException(f"Project ID {project_id} not found.")

        new_task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline
        )
        self.session.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)
        return new_task
    
    # ... (بقیه متدها: get_by_project, get_by_id, update, delete) ...

    def get_by_project(self, project_id: int) -> List[Task]:
        """Retrieves all tasks for a given project ID."""
        return self.session.query(Task).filter(Task.project_id == project_id).all()

    def get_by_id(self, project_id: int, task_id: int) -> Optional[Task]:
        """Retrieves a single task by its ID and project ID."""
        return self.session.query(Task).filter(
            Task.id == task_id,
            Task.project_id == project_id
        ).first()

    def update(
        self, 
        task: Task, 
        title: str, 
        description: Optional[str], 
        deadline: Optional[datetime], 
        status: TaskStatus, 
        closed_at: Optional[datetime]
    ) -> None:
        """Updates an existing task object and persists changes."""
        
        task.title = title
        task.description = description
        task.deadline = deadline
        task.status = status
        task.closed_at = closed_at
        
        self.session.commit()
        self.session.refresh(task)

    def delete(self, task: Task) -> None:
        """Deletes a task object."""
        self.session.delete(task)
        self.session.commit()
