# app/repositories/base.py
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

class ProjectRepository(ABC):
    @abstractmethod
    def get(self, project_id: int):
        pass

    @abstractmethod
    def list(self) -> List:
        pass

    @abstractmethod
    def add(self, project):
        pass

    @abstractmethod
    def delete(self, project):
        pass

class TaskRepository(ABC):
    @abstractmethod
    def get(self, task_id: int):
        pass

    @abstractmethod
    def list(self, *, project_id: int | None = None):
        pass

    @abstractmethod
    def add(self, task):
        pass

    @abstractmethod
    def delete(self, task):
        pass

    @abstractmethod
    def list_overdue(self, now: datetime):
        pass
