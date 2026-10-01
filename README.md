# Task Manager API
REST API to manage tasks with JWT authentication. Built with FastAPI, PostgreSQL & SQLAlchemy.

## Tech Stack 
| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migrations | Alembic |
| Auth | PyJWT + pwdlib (Argon2) |
| Dependency management | Poetry |


## Quick start (Docker)
The fastest way to run this project(no local python or PostgreSQL install needed)

### Prerequisites
-  Docker Desktop installed and running

### Run

```bash
git clone https://github.com/Stouve/EasyTaskManager
cd EasyTaskManager
docker compose up --build
```
On first run, Docker will:

1. Pull a PostgreSQL 18 image and start the database
2. Build the API image and install dependencies
3. Automatically run all Alembic migrations
4. Start the API with hot-reload enabled

Once you see **Application startup complete**. in the logs, open http://localhost:8000/docs to try the API via the interactive Swagger UI.

To stop everything:

```bash
docker compose down
```
(add -v if you also want to wipe the database volume and start fresh)

>Note: the credentials in docker-compose.yml are placeholders for local development only — never used in any real deployment.

## Manual Setup(without Docker)

### Prerequisites
- Python 3.11+
- PostgreSQL
- Poetry

### Setup

GIT
```bash
git clone https://github.com/Stouve/EasyTaskManager
poetry install
```
POSTGRESQL

Fill setup.sql with user/pwd and run 
```
psql -U postgres -f setup.sql
```

Copy `.env.example` into `.env` et fill with user/pwd :

```env
DATABASE_URL=postgresql://user:password@localhost:5432/tasks_db
```

> Previously SQLite : `sqlite:///./tasks.db`

### Migrations

```bash
poetry run alembic upgrade head
```

### Run

```bash
poetry run uvicorn app.main:app --reload
```

## Features

- ✅ Task management (CRUD)
- ✅ JWT Authentication (access + refresh tokens)
- ✅ Role-based access control (user / admin)
- ✅ Per-user task isolation (users only see their own tasks)
- ✅ Pagination & sorting on task listing
- ✅ Refresh token stored server-side (revocation support)
- ✅ Refresh token in httpOnly cookie (XSS protection)
- ✅ Password hashing with Argon2 (via pwdlib)
- ✅ Database migrations with Alembic

## Endpoints

| Method | Route | Description         |
|--------|---|---------------------|
| GET    | `/tasks` | List all tasks      |
| POST   | `/tasks` | Create Task         |
| GET    | `/tasks/{id}` | Get one Task        |
| PUT    | `/tasks/{id}` | Full Update Task    |
| PATCH  | `/tasks/{id}` | Partial Update Task |
| DELETE | `/tasks/{id}` | Delete Task         |

## Project Structure

```
app/
├── core/               # Business logic (no framework dependency)
│   ├── task.py         # Task domain entity
│   ├── user.py         # User domain entity & roles
│   ├── services.py     # Task service
│   └── auth_service.py # Auth service (register, login, tokens)
├── infrastructure/     # Database & persistence
│   ├── database.py     # Engine & session
│   ├── db_models.py    # SQLAlchemy TaskModel
│   ├── user_models.py  # SQLAlchemy UserModel & RefreshTokenModel
│   ├── models.py       # Centralized model imports (required for Alembic)
│   ├── repository.py   # Task repository
│   └── user_repository.py # User & refresh token repository
├── routers/            # HTTP layer
│   ├── task_router.py  # /tasks routes (protected)
│   └── auth_router.py  # /auth routes
├── schemas/            # Pydantic schemas (data validation)
│   ├── task_schema.py
│   ├── user_schema.py
│   └── pagination.py
├── security/           # Auth utilities
│   ├── jwt_handler.py  # JWT encode/decode (PyJWT)
│   ├── password_hasher.py # Argon2 hashing (pwdlib)
│   └── dependencies.py # FastAPI dependencies (get_current_user, require_role)
└── main.py
```