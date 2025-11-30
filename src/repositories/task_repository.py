from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update as sql_update
from src.models.task import Task, TaskStatus
from src.models.project import Project 
from datetime import datetime

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_id: int, title: str, description: str, status: TaskStatus, deadline: Optional[datetime]) -> Task:
        new_task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def get_by_id(self, project_id: int, task_id: int) -> Optional[Task]:
        # Query task by ID within a specific project
        stmt = select(Task).where(Task.project_id == project_id, Task.id == task_id)
        return self.db.scalars(stmt).one_or_none()
    
    def get_overdue_and_open_tasks(self) -> List[Task]:
        """Fetches tasks whose deadline has passed and status is not DONE."""
        stmt = select(Task).where(
            Task.deadline < datetime.now(),
            Task.status != TaskStatus.DONE
        )
        return self.db.scalars(stmt).all()
        
    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        stmt = select(Task).where(Task.project_id == project_id)
        return self.db.scalars(stmt).all()

    def update(self, task: Task, title: str, description: str, deadline: Optional[datetime], status: TaskStatus, closed_at: Optional[datetime] = None):
        task.title = title
        task.description = description
        task.deadline = deadline
        task.status = status
        task.closed_at = closed_at
        self.db.commit()
        
    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()
