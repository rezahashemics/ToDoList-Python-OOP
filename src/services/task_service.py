from typing import List, Optional
from datetime import datetime
from src.repositories.task_repository import TaskRepository
from src.repositories.project_repository import ProjectRepository
from src.models.task import Task, TaskStatus
from src.exceptions.repository_exceptions import NotFoundException 

class TaskService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def _parse_deadline(self, deadline: Optional[str]) -> Optional[datetime]:
        if not deadline:
            return None
        try:
            dt = datetime.fromisoformat(deadline)
            # Business Logic: Deadline must be in the future
            # if dt < datetime.now(): 
            #     raise ValueError("Deadline must be in the future")
            return dt
        except ValueError:
            raise ValueError("Invalid deadline format. Use YYYY-MM-DDTHH:MM:SS")

    def create_task(self, project_id: int, title: str, description: str, deadline: Optional[str]) -> Task:
        # Validation: Check if project exists
        if not self.project_repo.get_by_id(project_id):
            raise NotFoundException(f"Project ID {project_id} not found.")
            
        dt_deadline = self._parse_deadline(deadline)
        
        # Validation: Title length
        if len(title.split()) > 30:
            raise ValueError("Title must be <= 30 words")

        return self.task_repo.create(
            project_id=project_id,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            deadline=dt_deadline
        )
    
    def list_tasks_by_project(self, project_id: int) -> List[Task]:
        # Validation: Check if project exists
        if not self.project_repo.get_by_id(project_id):
            return [] # Or raise NotFoundException
            
        return self.task_repo.get_tasks_by_project(project_id)

    # ... (Implement update_task, delete_task, and update_task_status using the repository methods)
