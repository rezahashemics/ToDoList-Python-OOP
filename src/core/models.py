from typing import Optional
from datetime import datetime
from enum import Enum
# Import SQLAlchemy types and Base
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from src.db import Base # Import Base from our db setup

# TaskStatus remains the same (Python Enum)
class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

# Change Project and Task to inherit from Base
# Project is defined before Task because Task has a foreign key to Project

class Project(Base):
    __tablename__ = "projects" # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    
    # Relationship to tasks (back_populates is for bidirectional relationship)
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __str__(self):
        return f"Project {self.id}: {self.name}"

# Add validation logic to be used before adding/updating in repository (not directly in model)
# For simplicity, we are removing the word count validation from the __init__ of the model 
# and moving all necessary attributes to be handled by SQLAlchemy.

class Task(Base):
    __tablename__ = "tasks" # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True) # Foreign Key
    title = Column(String)
    description = Column(String, nullable=True)
    # Using SQLAlchemy's Enum type for TaskStatus
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO) 
    deadline = Column(DateTime, nullable=True)

    # Relationship back to the project
    project = relationship("Project", back_populates="tasks")

    def __str__(self):
        # Accessing the .value of the TaskStatus Enum for printing
        dl = self.deadline.isoformat() if self.deadline else "None"
        return f"Task {self.id}: {self.title} ({self.status.value}) Deadline: {dl}"

    # We can keep the update_status method as a utility
    def update_status(self, new_status: TaskStatus):
        self.status = new_status
