from typing import Dict, List, Optional
from src.core.models import Project, Task
import os
from dotenv import load_dotenv
from src.core.models import TaskStatus
from datetime import datetime

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

    # ... (rest of the file above remains the same)

    def update_task(self, project_id: int, task_id: int, title: str, description: str, deadline: Optional[str], status: str):
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("Task not found")
        # Validations (reuse logic similar to Task creation)
        if len(title.split()) > 30:
            raise ValueError("Title must be <= 30 words")
        if description and len(description.split()) > 150:
            raise ValueError("Description must be <= 150 words")
        dl = datetime.fromisoformat(deadline) if deadline else None
        if dl and dl < datetime.now():
            raise ValueError("Deadline must be in the future")
        try:
            new_status = TaskStatus(status)
        except ValueError:
            raise ValueError("Invalid status")
        # Apply updates
        task.title = title
        task.description = description
        task.deadline = dl
        task.status = new_status

    def delete_task(self, project_id: int, task_id: int):
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        # Remove the task if found, else no-op or error (per user story, show message in CLI)
        initial_len = len(project.tasks)
        project.tasks = [t for t in project.tasks if t.id != task_id]
        if len(project.tasks) == initial_len:
            raise ValueError("Task not found")



    def get_tasks_for_project(self, project_id: int) -> List[Task]:
        project = self.get_project(project_id)
        return project.tasks if project else []
