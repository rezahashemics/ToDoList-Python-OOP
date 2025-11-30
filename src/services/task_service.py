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
    def update_task(self, project_id: int, task_id: int, title: str, description: str, deadline: Optional[str], status: TaskStatus):
        task = self.task_repo.get_by_id(project_id=project_id, task_id=task_id)
        
        if not task:
            raise NotFoundException(f"Task ID {task_id} in project {project_id} not found.")

        dt_deadline = self._parse_deadline(deadline)
        
        # Logic for setting closed_at on status change
        closed_at = datetime.now() if status == TaskStatus.DONE and task.status != TaskStatus.DONE else None
        
        # Validation: Title length
        if len(title.split()) > 30:
            raise ValueError("Title must be <= 30 words")
            
        self.task_repo.update(
            task=task,
            title=title,
            description=description,
            deadline=dt_deadline,
            status=status,
            closed_at=closed_at
        )
        return task

    # 💡 متد جدید: Delete Task
    def delete_task(self, project_id: int, task_id: int):
        task = self.task_repo.get_by_id(project_id=project_id, task_id=task_id)
        
        if not task:
            # Note: We don't raise 404/NotFound here if the task doesn't exist 
            # as idempotent DELETE is often accepted (no change if already gone), 
            # but for consistency with other methods, we raise NotFound.
            raise NotFoundException(f"Task ID {task_id} in project {project_id} not found.")

        self.task_repo.delete(task)
