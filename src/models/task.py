from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks" 

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True) 
    title = Column(String)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO) 
    deadline = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True) # Added for autoclose feature
    
    # Relationship back to the project
    project = relationship("Project", back_populates="tasks")

    def __str__(self):
        dl = self.deadline.isoformat() if self.deadline else "None"
        return f"Task {self.id}: {self.title} ({self.status.value}) Deadline: {dl}"
