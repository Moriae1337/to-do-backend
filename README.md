# ToDo Web App Backend

This is a **FastAPI** backend for a simple ToDo web application. It provides a RESTful API for managing tasks.

---

## Features

- Display a list of all tasks
- Add a new task
- Delete a task
- Search for tasks
- Mark a task as done/undone
- Filter tasks by status (all / done / undone)
- Assign priority to tasks (1–10)
- Sort tasks by priority ascending/descending

---

## Tech Stack

- **Backend:** Python 3.12+, FastAPI, SQLAlchemy (async), PostgreSQL/SQLite
- **Testing:** pytest, httpx
- **Documentation:** OpenAPI (Swagger UI), Postman collection

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Moriae1337/to-do-backend.git
cd todo-backend
```

```bash
docker-compose up --build
```

backend - FastAPI app at http://localhost:8000

## API Documentation

- **Deployed Backend**: [https://to-do-backend-zva2.onrender.com](https://to-do-backend-zva2.onrender.com)
- **Swagger UI** (interactive API docs): [http://localhost:8000/docs](http://localhost:8000/docs)
- **Postman Collection** (import and test endpoints): [ToDo Web App Collection](https://www.postman.com/moriae/workspace/todo-web-app/collection/40946319-0ddf086e-f0cf-42df-a6d6-106ff4007761?action=share&creator=40946319&active-environment=40946319-c5a89a6e-658d-4c4c-9ac0-adfdea1c8250)

## Database & Migrations

Run migrations inside the backend container:

```bash
docker-compose exec backend alembic upgrade head
```

change .env configuration file to smth like this:

```bash
APP_VERSION=1.0.0
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
DEBUG=True
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tododb
POSTGRES_HOST=db
POSTGRES_PORT=5432
HOST=0.0.0.0
PORT=8000
```
