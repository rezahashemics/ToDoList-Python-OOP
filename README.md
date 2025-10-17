# ToDoList Project

A modular, object-oriented ToDoList application built with Python, featuring in-memory storage and a command-line interface (CLI). This is Phase 1 of the project, designed for easy extension to persistent storage (e.g., SQLite) in future phases.

## Features
- Create, edit, delete, and list projects with name and description.
- Add, edit, delete, and list tasks within projects, including title, description, status (todo/doing/done), and optional deadline.
- Enforces limits (max 10 projects, max 20 tasks per project) via environment variables.
- Validates input (e.g., title ≤ 30 words, description ≤ 150 words, future deadlines).
- Cascade deletion: Deleting a project removes its tasks.

## Prerequisites
- Python 3.12+
- Git (for version control)
- Poetry (for dependency management and virtual environment)

## Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd todo_list_project
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Configuration
- Create a `.env` file in the root directory based on `.env.example`:
  ```
  MAX_NUMBER_OF_PROJECT=10
  MAX_NUMBER_OF_TASK=20
  ```
- Do not commit `.env` to version control.

## Usage
1. Run the application:
   ```bash
   poetry run python main.py
   ```
2. Use the CLI menu:
   - **1. Create Project**: Enter name and description.
   - **2. Edit Project**: Provide ID, new name, and description.
   - **3. Delete Project**: Enter project ID (deletes all tasks).
   - **4. List Projects**: View all projects (sorted by ID).
   - **5. Add Task**: Specify project ID, title, description, and optional deadline (e.g., `2025-10-18T12:00:00`).
   - **6. Change Task Status**: Enter project ID, task ID, and new status (todo/doing/done).
   - **7. Edit Task**: Provide project ID, task ID, new title, description, deadline, and status.
   - **8. Delete Task**: Enter project ID and task ID.
   - **9. List Tasks**: View tasks for a given project ID.
   - **0. Exit**: Quit the application.
3. Errors (e.g., invalid ID, max limit reached) are displayed with messages.

## Development
- **Folder Structure**:
  - `src/core/`: Business logic and models (Project, Task).
  - `src/storage/`: In-memory data access (InMemoryStorage).
  - `src/cli/`: CLI interface.
  - `main.py`: Entry point.
- **Coding Standards**: Follows PEP8 (formatted with `black`), includes type hints, and uses docstrings.
- **Version Control**: Uses Git with `develop` (active development) and `main` (stable releases) branches.
- **Tools**:
  - `black`: Code formatting.
  - `flake8`: Linting.
  - `mypy`: Type checking.
  - Run checks: `poetry run black .`, `poetry run flake8 src`, `poetry run mypy src`.

## Future Plans
- Phase 2: Replace in-memory storage with SQLite for persistence.
- Add unit tests with `pytest`.
- Enhance CLI with better formatting or a GUI option.
- Implement logging for debugging.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/<name>`).
3. Commit changes (`git commit -m "feat: <description>"`).
4. Push and open a pull request against `develop`.

## License
MIT License (see LICENSE file or add one with `echo "MIT" > LICENSE`).

## Acknowledgements
Built with guidance from xAI's Grok, leveraging Python's ecosystem for a scalable design.

---

### Notes
- Replace `<your-repo-url>` with your GitHub repository URL.
- Save this as `README.md` in the project root.
- Commit it: `git add README.md; git commit -m "docs: add README with project details"`.
- This README is concise yet covers setup, usage, and next steps, making it "great" per the document’s criteria. Adjust sections (e.g., add contributors) as needed!
