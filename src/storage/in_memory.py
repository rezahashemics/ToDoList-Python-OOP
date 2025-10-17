from typing import Dict, List, Optional
from src.core.models import Project, Task
import os
from dotenv import load_dotenv
from src.core.models import TaskStatus

load_dotenv()  # Load .env
MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", 10))
MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASK", 20))

class InMemoryStorage:
    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self.next_project_id = 1
        self.next_task_id = 1

    def create_project(self, name: str, description: str) -> Project:
        if len(self.projects) >= MAX_PROJECTS:
            raise ValueError("Max projects reached")
        if any(p.name == name for p in self.projects.values()):
            raise ValueError("Project name duplicate")
        project = Project(self.next_project_id, name, description)
        self.projects[self.next_project_id] = project
        self.next_project_id += 1
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.projects.get(project_id)

    def update_project(self, project_id: int, name: str, description: str):
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        if any(p.name == name and p.id != project_id for p in self.projects.values()):
            raise ValueError("Project name duplicate")
        project.name = name
        project.description = description

    def delete_project(self, project_id: int):
        if project_id not in self.projects:
            raise ValueError("Project not found")
        del self.projects[project_id]  # Cascade: tasks are in project, so auto-deleted

    def get_all_projects(self) -> List[Project]:
        return list(self.projects.values())

    # Task methods
    def create_task(self, project_id: int, title: str, description: str, status: str, deadline: Optional[str]) -> Task:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        if len(project.tasks) >= MAX_TASKS:
            raise ValueError("Max tasks reached")
        from datetime import datetime
        dl = datetime.fromisoformat(deadline) if deadline else None
        task = Task(self.next_task_id, title, description, TaskStatus(status), dl)
        project.add_task(task)
        self.next_task_id += 1
        return task

    def update_task_status(self, project_id: int, task_id: int, new_status: str):
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("Task not found")
        task.update_status(TaskStatus(new_status))

    def update_task(self, project_id: int, task_id: int, title: str, description: str, deadline: Optional[str]):
        # Similar to above, find task and update fields with validations
        return
        
    def delete_task(self, project_id: int, task_id: int):
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        project.tasks = [t for t in project.tasks if t.id != task_id]

    def get_tasks_for_project(self, project_id: int) -> List[Task]:
        project = self.get_project(project_id)
        return project.tasks if project else []
