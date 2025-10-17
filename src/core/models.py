from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task:
    def __init__(self, id: int, title: str, description: str = "", status: TaskStatus = TaskStatus.TODO, deadline: Optional[datetime] = None):
        if len(title.split()) > 30:
            raise ValueError("Title must be <= 30 words")
        if description and len(description.split()) > 150:
            raise ValueError("Description must be <= 150 words")
        if deadline and deadline < datetime.now():
            raise ValueError("Deadline must be in the future")
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline

    def update_status(self, new_status: TaskStatus):
        self.status = new_status

    # Add docstrings and other methods as needed (e.g., __str__ for printing)
    def __str__(self):
        return f"Task {self.id}: {self.title} ({self.status.value}) Deadline: {self.deadline}"

class Project:
    def __init__(self, id: int, name: str, description: str = ""):
        if len(name.split()) > 30:
            raise ValueError("Name must be <= 30 words")
        if description and len(description.split()) > 150:
            raise ValueError("Description must be <= 150 words")
        self.id = id
        self.name = name
        self.description = description
        self.tasks: list[Task] = []

    # Add task method with validation
    def add_task(self, task: Task):
        self.tasks.append(task)

    # Other methods: edit, delete task, etc.
    def __str__(self):
        return f"Project {self.id}: {self.name}"
