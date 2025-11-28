# tests/test_task_autoclose.py
import pytest
from datetime import datetime, timedelta
from app.models.task import Task, TaskStatus
from app.services.task_service import TaskService
from app.db.session import SessionLocal
from app.models.project import Project

@pytest.fixture
def session():
    session = SessionLocal()
    # optionally: create temp schema or use a test DB
    yield session
    session.rollback()
    session.close()

def test_autoclose_overdue(session):
    # create a project
    p = Project(name="test", description="x")
    session.add(p)
    session.commit()
    # create overdue task
    t = Task(title="old", deadline=datetime.utcnow() - timedelta(days=2), status=TaskStatus.todo, project_id=p.id)
    session.add(t)
    session.commit()

    service = TaskService()
    count = service.autoclose_overdue()
    assert count >= 1
    # refresh t
    session.refresh(t)
    assert t.status == TaskStatus.done
    assert t.closed_at is not None
