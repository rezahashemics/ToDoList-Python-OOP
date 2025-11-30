from sqlalchemy.orm import Session
from src.repositories.task_repository import TaskRepository
from src.models.task import TaskStatus
from datetime import datetime

class AutocloseOverdueTasksCommand:
    """
    Command to automatically close tasks that are past their deadline
    and still in 'todo' or 'doing' status.
    """
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def execute(self) -> int:
        """
        Finds overdue tasks and changes their status to DONE.
        Returns the number of tasks closed.
        """
        closed_count = 0
        
        # 1. Get all tasks that are overdue and not yet done (using repo query)
        overdue_tasks = self.task_repo.get_overdue_and_open_tasks()

        for task in overdue_tasks:
            # 2. Update the task status and set closed_at timestamp
            task.status = TaskStatus.DONE
            task.closed_at = datetime.now()
            
            # Note: We are committing one by one inside the loop 
            # for simplicity, but a single batch commit is often better for performance.
            self.task_repo.db.commit() 
            closed_count += 1
            
        return closed_count
