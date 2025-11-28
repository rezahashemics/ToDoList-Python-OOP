# app/repositories/project_repository.py
from typing import List
from sqlalchemy import select
from app.models import Project
from app.db.session import SessionLocal

class SqlAlchemyProjectRepository:
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def get(self, project_id: int) -> Project | None:
        stmt = select(Project).where(Project.id == project_id)
        return self.session.execute(stmt).scalars().first()

    def list(self) -> List[Project]:
        stmt = select(Project)
        return self.session.execute(stmt).scalars().all()

    def add(self, project: Project) -> Project:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        self.session.delete(project)
        self.session.commit()
