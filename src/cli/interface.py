# Remove the old in_memory import
# from src.storage.in_memory import InMemoryStorage 
from src.storage.sqlalchemy_storage import SQLAlchemyStorage # Import the new storage
from src.db import SessionLocal, get_db # Import session handling

class CLI:
    def __init__(self):
        # No longer initializing storage here directly.
        # We will create a session in run() loop for each operation
        pass

    def _get_storage(self) -> SQLAlchemyStorage:
        """Helper to get a new database session and SQLAlchemyStorage instance."""
        # Use a database session generator (like get_db)
        # Note: In a CLI, this is simpler, but for a complex app, each command 
        # should ideally manage its own session context.
        # For simplicity, we open a new session for each *run* of the CLI:
        db = SessionLocal() 
        return SQLAlchemyStorage(db)
    
    def run(self):
        # Initialize storage with a session
        # The main issue with this approach is that the session lives for the 
        # entire lifetime of the CLI run. A better way (for production) is
        # to create a new session for *each* command execution.
        
        # Let's use the better approach: create session inside the try block
        
        while True:
            print("\nOptions:\n 1. Create Project\n 2. Edit Project")
            print(" 3. Delete Project\n 4. List Projects")
            print(" 5. Add Task\n 6. Change Task Status\n 7. Edit Task")
            print(" 8. Delete Task\n 9. List Tasks\n 0. Exit")
            choice = input("Choose: ").strip()
            
            # Start session block
            db_session = SessionLocal()
            try:
                # Use the storage instance with the current session
                storage = SQLAlchemyStorage(db_session)
                
                if choice == "1":  # Create Project
                    name = input("Project name: ").strip()
                    desc = input("Description: ").strip()
                    proj = storage.create_project(name, desc) # Use storage
                    print(f"Created: {proj}")
                
                elif choice == "2":  # Edit Project
                    proj_id = int(input("Project ID: "))
                    new_name = input("New name: ").strip()
                    new_desc = input("New description: ").strip()
                    storage.update_project(proj_id, new_name, new_desc)
                    print("Project updated")
                    
                # ... (implement all other elif blocks using 'storage' instead of 'self.storage')
                elif choice == "3":  # Delete Project
                    proj_id = int(input("Project ID: "))
                    storage.delete_project(proj_id)
                    print("Project deleted (with tasks)")
                
                elif choice == "4":  # List Projects
                    projects = storage.get_all_projects()
                    if not projects:
                        print("No projects exist")
                    else:
                        for p in projects: # Projects are already ordered by id in storage
                            print(f"{p.id}: {p.name} - {p.description}")

                elif choice == "5":  # Add Task
                    proj_id = int(input("Project ID: "))
                    title = input("Title: ").strip()
                    desc = input("Description: ").strip()
                    status = "todo"  # Default
                    deadline = (
                        input("Deadline (YYYY-MM-DDTHH:MM:SS or empty): ").strip()
                        or None
                    )
                    task = storage.create_task(
                        proj_id, title, desc, status, deadline
                    )
                    print(f"Added: {task}")
                
                elif choice == "6":  # Change Task Status
                    proj_id = int(input("Project ID: "))
                    task_id = int(input("Task ID: "))
                    new_status = input("New status (todo/doing/done): ").strip()
                    storage.update_task_status(proj_id, task_id, new_status)
                    print("Status updated")

                elif choice == "7":  # Edit Task
                    proj_id = int(input("Project ID: "))
                    task_id = int(input("Task ID: "))
                    title = input("New title: ").strip()
                    desc = input("New description: ").strip()
                    deadline = (
                        input("New deadline (YYYY-MM-DDTHH:MM:SS or empty): ").strip()
                        or None
                    )
                    status = input("New status (todo/doing/done): ").strip()
                    storage.update_task(
                        proj_id, task_id, title, desc, deadline, status
                    )
                    print("Task updated")
                    
                elif choice == "8":  # Delete Task
                    proj_id = int(input("Project ID: "))
                    task_id = int(input("Task ID: "))
                    storage.delete_task(proj_id, task_id)
                    print("Task deleted")
                    
                elif choice == "9":  # List Tasks for Project
                    proj_id = int(input("Project ID: "))
                    tasks = storage.get_tasks_for_project(proj_id)
                    if not tasks:
                        print("No tasks or project not found")
                    else:
                        for t in tasks:
                            # t.__str__ uses t.deadline.isoformat()
                            print(str(t)) 
                            
                elif choice == "0":
                    break
                    
                else:
                    print("Invalid choice")
                    
            except ValueError as e:
                # Rollback the transaction on error
                db_session.rollback()
                print(f"Error: {e}")
            except Exception as e:
                db_session.rollback()
                print(f"Unexpected error: {e}")
            finally:
                # Close the session after each command block
                db_session.close()
