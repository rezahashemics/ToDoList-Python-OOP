# ToDoList Project - RESTful Web API

A modular, object-oriented ToDoList application built with Python. The project has evolved from an initial CLI/In-Memory structure to a **high-performance RESTful Web API** using **FastAPI** and a **PostgreSQL** database.

## Completed Phases

| Phase | Focus | Technologies |
| :--- | :--- | :--- |
| **Phase 1** | Initial Design & CLI | OOP, In-Memory Storage, CLI |
| **Phase 2** | Persistence & Architecture | **PostgreSQL**, **SQLAlchemy ORM**, **Alembic**, Repository Pattern |
| **Phase 3 & 4** | Web API & Testing | **FastAPI**, **Pydantic**, Layered Architecture, Postman/Swagger UI Testing |

## Features

- **Full CRUD Operations**: Implemented for both **Projects** and **Tasks** (as nested resources).
- **Layered Architecture**: Strict separation of concerns (Router → Service → Repository) ensuring maintainability and clean domain logic.
- **Data Validation & Serialization**: Uses **Pydantic** for robust request validation and standardized response formatting.
- **Business Logic Enforcement**: Automatically sets the **`closed_at`** timestamp when a Task's status is updated to `"done"`. Conversely, it resets `closed_at` to `null` if the task is reopened.
- **Database Management**: Utilizes **Alembic** for efficient and version-controlled schema migrations.
- **Auto-Documentation**: All API endpoints are automatically documented and accessible via **Swagger UI**.

## Prerequisites
- Python 3.12+
- Git
- **Poetry** (for dependency management and virtual environment)
- **Docker** (to run the PostgreSQL database)

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd todo_list_project
    ```
2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```
3.  **Configure Environment:**
    - Create a `.env` file in the root directory. It must contain the database connection string, e.g.:
      ```
      DATABASE_URL=postgresql://user:password@db:5432/todo_db
      ```
4.  **Run PostgreSQL with Docker:**
    - Start your PostgreSQL container (assuming you use a standard setup like `docker-compose`):
      ```bash
      docker-compose up -d postgres
      ```
5.  **Run Database Migrations (Alembic):**
    ```bash
    poetry shell
    alembic upgrade head
    ```

## Usage (Running the Web API)

1.  **Activate the virtual environment:**
    ```bash
    poetry shell
    ```
2.  **Run the Uvicorn server:**
    ```bash
    uvicorn main:app --reload
    ```
3.  **Access the API:**
    - **Interactive Docs (Swagger UI):** Open your browser to `http://127.0.0.1:8000/docs`.
    - **Key Endpoints:**

| Resource | Method | Path | Description |
| :--- | :--- | :--- | :--- |
| Projects | `POST` | `/v1/projects/` | Create a new project |
| Tasks | `GET` | `/v1/projects/{project_id}/tasks/` | List all tasks for a project |
| Tasks | `PUT` | `/v1/projects/{project_id}/tasks/{task_id}` | Update a specific task |
| Tasks | `DELETE` | `/v1/projects/{project_id}/tasks/{task_id}` | Delete a specific task |

## Architecture Overview

| Layer | Responsibility |
| :--- | :--- |
| **Router** | Handles HTTP routing, request/response serialization (Pydantic), and maps Service-level exceptions (`NotFoundException`) to HTTP status codes (`404`). |
| **Service** | Contains all core business logic (e.g., task status handling, input validation, coordinating data access). |
| **Repository** | Manages direct interaction with the database via SQLAlchemy, abstracting data fetching and persistence. |

## Future Plans
- Implement User Authentication and Authorization.
- Add comprehensive Unit Tests (using `pytest`) for Service and Repository layers.
- Implement Rate Limiting to protect API endpoints.

## License
MIT License

## Acknowledgements
Built with guidance from xAI's Grok, utilizing modern Python development standards.
