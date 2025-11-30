from src.db.session import SessionLocal
from src.repositories.project_repository import ProjectRepository
from src.repositories.task_repository import TaskRepository
from src.services.project_service import ProjectService
from src.services.task_service import TaskService
from src.exceptions.repository_exceptions import NotFoundException 
from src.models.task import TaskStatus
from sqlalchemy.orm import Session # For type hinting (optional but good practice)

class CLI:
    def display_menu(self):
        """Prints the menu options to the console."""
        print("-" * 30)
        print("To Do List Manager (PostgreSQL/SQLAlchemy)")
        print("-" * 30)
        
        # Project Operations
        print("  Projects:")
        print("    1 - Create Project")
        print("    2 - Update Project")
        print("    3 - Delete Project")
        print("    4 - List Projects")
        print("-" * 30)

        # Task Operations
        print("  Tasks:")
        print("    5 - Add Task to Project")
        print("    6 - Update Task")
        print("    7 - Delete Task")
        print("    8 - Change Task Status (TODO/DOING/DONE)")
        print("    9 - List Tasks by Project")
        print("-" * 30)
        
        # Other
        print("  Other:")
        print("    0 - Exit")
        print("-" * 30)

    def run(self):
        while True:
            # 1. Display the menu
            self.display_menu() 
            choice = input("Choose: ").strip()
            
            if choice == "0":
                print("\nExiting application. Goodbye!")
                break
            
            # --- Dependency Injection and Database Block ---
            # A new session is opened for each command execution
            db_session: Session = SessionLocal()
            try:
                # 2. Instantiate Repositories (Depend on the session)
                project_repo = ProjectRepository(db_session)
                task_repo = TaskRepository(db_session)
                
                # 3. Instantiate Services (Depend on Repositories)
                project_service = ProjectService(repo=project_repo)
                task_service = TaskService(task_repo=task_repo, project_repo=project_repo)
                # ----------------------------------
                
                if choice == "1":  # Create Project
                    name = input("Project name: ").strip()
                    desc = input("Description: ").strip()
                    proj = project_service.create_project(name, desc) 
                    print(f"\n✅ Created: {proj}")
                
                elif choice == "4":  # List Projects
                    projects = project_service.list_projects()
                    print("\n--- Project List ---")
                    if not projects:
                        print("No projects exist.")
                    else:
                        for p in projects:
                            # Note: The str method in models/project.py should be robust
                            print(f"ID {p.id}: {p.name} - {p.description}")
                    print("-" * 20)
                            
                elif choice == "5":  # Add Task
                    try:
                        proj_id = int(input("Project ID: "))
                    except ValueError:
                        print("\n❌ Invalid Project ID format. Must be an integer.")
                        continue
                        
                    title = input("Title: ").strip()
                    desc = input("Description: ").strip()
                    deadline = (
                        input("Deadline (YYYY-MM-DDTHH:MM:SS or empty): ").strip()
                        or None
                    )
                    
                    task = task_service.create_task(
                        proj_id, title, desc, deadline
                    )
                    print(f"\n✅ Added: {task}")
                
                elif choice == "9":  # List Tasks for Project
                    try:
                        proj_id = int(input("Project ID: "))
                    except ValueError:
                        print("\n❌ Invalid Project ID format. Must be an integer.")
                        continue

                    tasks = task_service.list_tasks_by_project(proj_id)
                    print(f"\n--- Tasks for Project ID {proj_id} ---")
                    if not tasks and not project_repo.get_by_id(proj_id):
                        print(f"Project ID {proj_id} not found.")
                    elif not tasks:
                         print("No tasks in this project.")
                    else:
                        for t in tasks:
                            print(f"ID {t.id}: {t.title} ({t.status.value}) Deadline: {t.deadline if t.deadline else 'N/A'}")
                    print("-" * 30)

                elif choice in ("2", "3", "6", "7", "8"):
                    print("\n⚠️ Feature not yet fully implemented in the service layer.")

                else:
                    print("\n❌ Invalid choice. Please select an option from the menu.")
                    
            except (ValueError, NotFoundException) as e:
                # Catch business logic errors (ValueError) or not found errors (NotFoundException)
                db_session.rollback()
                print(f"\n❌ Error: {e}")
            except Exception as e:
                # Catch unexpected database errors
                db_session.rollback()
                print(f"\n❌ Unexpected System Error: {type(e).__name__}: {e}")
            finally:
                # Close the session regardless of success or failure
                db_session.close()
