# app/repositories/task_repository.py
from typing import List
from datetime import datetime
from sqlalchemy import select, update, delete
from app.models import Task
from app.db.session import SessionLocal

class SqlAlchemyTaskRepository:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def get(self, task_id: int) -> Task | None:
        stmt = select(Task).where(Task.id == task_id)
        return self.session.execute(stmt).scalars().first()

    def list(self, *, project_id: int | None = None) -> List[Task]:
        stmt = select(Task)
        if project_id is not None:
            stmt = stmt.where(Task.project_id == project_id)
        stmt = stmt.order_by(Task.created_at.desc())
        return self.session.execute(stmt).scalars().all()

    def add(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()

    def list_overdue(self, now: datetime):
        stmt = select(Task).where(Task.deadline != None).where(Task.status != "done").where(Task.deadline < now)
        return self.session.execute(stmt).scalars().all()
