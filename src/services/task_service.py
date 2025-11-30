from src.repositories.task_repository import TaskRepository
from src.exceptions.repository_exceptions import NotFoundException
from src.models.task import Task, TaskStatus
from typing import List, Optional
from datetime import datetime
from dateutil import parser as date_parser # 💡 فرض می‌کنیم dateutil نصب شده است

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    # 💡 متد کمکی برای واکشی تسک (اختیاری اما برای Update حیاتی است)
    def get_task_by_id(self, project_id: int, task_id: int) -> Task:
        """Retrieves a single task by its ID and project ID, raising 404 if not found."""
        task = self.task_repo.get_by_id(project_id, task_id)
        if not task:
            raise NotFoundException(f"Task ID {task_id} not found in Project ID {project_id}")
        return task
        
    def create_task(self, project_id: int, title: str, description: Optional[str], deadline: Optional[str]) -> Task:
        
        deadline_dt = date_parser.parse(deadline) if deadline else None

        return self.task_repo.add(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline_dt
        )
    
    def list_tasks_by_project(self, project_id: int) -> List[Task]:
        """Retrieves all tasks for a specific project."""
        return self.task_repo.get_by_project(project_id)
    
    # ----------------------------------------------------
    # 💡 منطق به‌روزرسانی تسک (Update)
    # ----------------------------------------------------
    def update_task(
        self, 
        project_id: int, 
        task_id: int, 
        title: str, 
        description: Optional[str], 
        deadline: Optional[str], 
        status: TaskStatus
    ) -> Task:
        """Updates an existing task with business logic for status change."""

        # 1. واکشی تسک موجود
        task = self.task_repo.get_by_id(project_id, task_id) 
        if not task:
            # 💡 در صورت پیدا نشدن، خطا پرتاب می‌شود که توسط Router به 404 تبدیل می‌شود
            raise NotFoundException(f"Task ID {task_id} not found in Project ID {project_id}.")

        # 2. تبدیل رشته deadline به datetime
        deadline_dt = date_parser.parse(deadline) if deadline else None
        
        # 3. اعمال منطق تجاری برای closed_at
        closed_at = task.closed_at
        
        # سناریو ۱: تغییر وضعیت به DONE
        if status == TaskStatus.DONE and task.status != TaskStatus.DONE:
            closed_at = datetime.now()
        
        # سناریو ۲: باز شدن مجدد تسک (تغییر از DONE به وضعیت دیگر)
        elif status != TaskStatus.DONE and task.closed_at:
             closed_at = None
        
        # 4. به‌روزرسانی در Repository
        self.task_repo.update(
            task=task,
            title=title,
            description=description,
            deadline=deadline_dt,
            status=status,
            closed_at=closed_at
        )
        return task

    def delete_task(self, project_id: int, task_id: int):
        task = self.task_repo.get_by_id(project_id, task_id) 
        if not task:
            raise NotFoundException(f"Task ID {task_id} not found in Project ID {project_id}.")
        self.task_repo.delete(task)
