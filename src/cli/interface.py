from src.storage.in_memory import InMemoryStorage


class CLI:
    def __init__(self):
        self.storage = InMemoryStorage()

    def run(self):
        while True:
            print("\nOptions:\n 1. Create Project\n 2. Edit Project")
            print(" 3. Delete Project\n 4. List Projects")
            print(" 5. Add Task\n 6. Change Task Status\n 7. Edit Task")
            print(" 8. Delete Task\n 9. List Tasks\n 0. Exit")
            choice = input("Choose: ").strip()
            try:
                if choice == "1":  # Create Project
                    name = input("Project name: ").strip()
                    desc = input("Description: ").strip()
                    proj = self.storage.create_project(name, desc)
                    print(f"Created: {proj}")
                elif choice == "2":  # Edit Project
                    proj_id = int(input("Project ID: "))
                    new_name = input("New name: ").strip()
                    new_desc = input("New description: ").strip()
                    self.storage.update_project(proj_id, new_name, new_desc)
                    print("Project updated")
                elif choice == "3":  # Delete Project
                    proj_id = int(input("Project ID: "))
                    self.storage.delete_project(proj_id)
                    print("Project deleted (with tasks)")
                elif choice == "4":  # List Projects
                    projects = self.storage.get_all_projects()
                    if not projects:
                        print("No projects exist")
                    else:
                        for p in sorted(projects, key=lambda x: x.id):
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
                    task = self.storage.create_task(
                        proj_id, title, desc, status, deadline
                    )
                    print(f"Added: {task}")
                elif choice == "6":  # Change Task Status
                    proj_id = int(input("Project ID: "))
                    task_id = int(input("Task ID: "))
                    new_status = input("New status (todo/doing/done): ").strip()
                    self.storage.update_task_status(proj_id, task_id, new_status)
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
                    self.storage.update_task(
                        proj_id, task_id, title, desc, deadline, status
                    )
                    print("Task updated")
                elif choice == "8":  # Delete Task
                    proj_id = int(input("Project ID: "))
                    task_id = int(input("Task ID: "))
                    self.storage.delete_task(proj_id, task_id)
                    print("Task deleted")
                elif choice == "9":  # List Tasks for Project
                    proj_id = int(input("Project ID: "))
                    tasks = self.storage.get_tasks_for_project(proj_id)
                    if not tasks:
                        print("No tasks or project not found")
                    else:
                        for t in tasks:
                            dl = t.deadline.isoformat() if t.deadline else "None"
                            print(
                                f"{t.id}: {t.title} ({t.status.value}) Deadline: {dl}"
                            )
                elif choice == "0":
                    break
                else:
                    print("Invalid choice")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
