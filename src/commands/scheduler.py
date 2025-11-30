import schedule
import time
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.repositories.task_repository import TaskRepository
from src.commands.autoclose_overdue import AutocloseOverdueTasksCommand

# Function that runs the command
def run_autoclose_command():
    # 💡 A new session is created for each scheduled run
    db: Session = SessionLocal() 
    try:
        task_repo = TaskRepository(db)
        command = AutocloseOverdueTasksCommand(task_repo)
        
        count = command.execute()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Auto-closed {count} overdue tasks.")
    except Exception as e:
        db.rollback()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR during autoclose: {e}")
    finally:
        db.close()

def start_scheduler():
    # Schedule the command to run every 1 minute
    schedule.every(1).minutes.do(run_autoclose_command)
    print("Scheduler started. Overdue task check runs every 1 minute.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # To run this standalone, you can execute this file directly: 
    # python src/commands/scheduler.py 
    start_scheduler()
