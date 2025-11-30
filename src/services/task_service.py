from src.repositories.task_repository import TaskRepository
from src.repositories.project_repository import ProjectRepository
from src.models.task import Task, TaskStatus
from src.exceptions.repository_exceptions import NotFoundException
from typing import List, Optional
from datetime import datetime
from dateutil import parser as date_parser

class TaskService:
    """
    Handles business logic and domain validation for Task operations.
    Requires both Task and Project Repositories for cross-resource checks.
    """
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def _parse_deadline(self, deadline_str: Optional[str]) -> Optional[datetime]:
        """Parses a string deadline into a datetime object."""
        if not deadline_str:
            return None
        try:
            return date_parser.parse(deadline_str)
        except date_parser.ParserError:
            raise ValueError("Invalid date format for deadline. Use ISO format (e.g., YYYY-MM-DDTHH:MM:SS).")

    def create_task(self, project_id: int, title: str, description: Optional[str], deadline: Optional[str]) -> Task:
        """Creates a new task within a specified project."""
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundException(f"Project ID {project_id} not found.")

        # Validation: Title length
        if len(title.split()) > 30:
            raise ValueError("Title must be <= 30 words.")
        
        dt_deadline = self._parse_deadline(deadline)
        
        return self.task_repo.add(
            project_id=project_id,
            title=title,
            description=description,
            deadline=dt_deadline
        )

    def list_tasks_by_project(self, project_id: int) -> Optional[List[Task]]:
        """Retrieves all tasks for a given project ID."""
        project = self.project_repo.get_by_id(project_id)
        if not project:
             # Returning None/[] and handling 404 in the router is cleaner
             raise NotFoundException(f"Project ID {project_id} not found.")

        return self.task_repo.get_by_project(project_id)

    def update_task(
        self, 
        project_id: int, 
        task_id: int, 
        title: str, 
        description: Optional[str], 
        deadline: Optional[str], 
        status: TaskStatus
    ) -> Task:
        """Updates an existing task, handles status change logic."""
        
        task = self.task_repo.get_by_id(project_id=project_id, task_id=task_id)
        
        if not task:
            raise NotFoundException(f"Task ID {task_id} in project {project_id} not found.")

        # Validation: Title length
        if len(title.split()) > 30:
            raise ValueError("Title must be <= 30 words.")

        dt_deadline = self._parse_deadline(deadline)
        
        # Business Logic: Set closed_at if status changes to DONE
        closed_at = None
        if status == TaskStatus.DONE and task.status != TaskStatus.DONE:
            closed_at = datetime.now()
        elif status != TaskStatus.DONE and task.closed_at:
             # Reset closed_at if task is reopened
             closed_at = None
        elif task.closed_at:
             # Keep existing closed_at if status is DONE and no change
             closed_at = task.closed_at


        self.task_repo.update(
            task=task,
            title=title,
            description=description,
            deadline=dt_deadline,
            status=status,
            closed_at=closed_at
        )
        return task

    def delete_task(self, project_id: int, task_id: int):
        """Deletes a task by ID."""
        task = self.task_repo.get_by_id(project_id=project_id, task_id=task_id)
        
        if not task:
            raise NotFoundException(f"Task ID {task_id} in project {project_id} not found.")

        self.task_repo.delete(task)
