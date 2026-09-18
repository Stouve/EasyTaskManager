# Task Manager API
API REST to manage Tasks. Built with FastAPI, PostgreSQL & SQLAlchemy

## Tech Stack 
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Poetry

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

## Endpoints

| Method | Route | Description         |
|--------|---|---------------------|
| GET    | `/tasks` | List all tasks      |
| POST   | `/tasks` | Create Task         |
| GET    | `/tasks/{id}` | Get one Task        |
| PUT    | `/tasks/{id}` | Full Update Task    |
| PATCH  | `/tasks/{id}` | Partial Update Task |
| DELETE | `/tasks/{id}` | Delete Task         |