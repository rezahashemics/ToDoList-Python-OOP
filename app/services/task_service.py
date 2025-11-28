# app/services/task_service.py
from datetime import datetime
from typing import List
from app.repositories.task_repository import SqlAlchemyTaskRepository
from app.models import Task, TaskStatus

class TaskService:
    def __init__(self, repo: SqlAlchemyTaskRepository = None):
        self.repo = repo or SqlAlchemyTaskRepository()

    def create_task(self, title: str, description: str | None = None, deadline: datetime | None = None, project_id: int | None = None) -> Task:
        task = Task(title=title, description=description, deadline=deadline, project_id=project_id)
        return self.repo.add(task)

    def list_tasks(self, project_id: int | None = None) -> List[Task]:
        return self.repo.list(project_id=project_id)

    def autoclose_overdue(self, now: datetime = None) -> int:
        now = now or datetime.utcnow()
        overdue = self.repo.list_overdue(now)
        count = 0
        for t in overdue:
            t.status = TaskStatus.done
            t.closed_at = datetime.utcnow()
            # session commit via repo.add or direct session - easier to rely on repo.session
            self.repo.session.add(t)
            count += 1
        if count:
            self.repo.session.commit()
        return count
