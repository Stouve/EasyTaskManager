# Task Manager API
API REST to manage Tasks. Built with FastAPI, PostgreSQL & SQLAlchemy

## Tech Stack 
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Poetry

## Installation

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
PostgreSQL 
```
# Login with superuser
psql -U postgres

# Create user
CREATE USER MyUser WITH PASSWORD 'MyPassword';

# Create Database
CREATE DATABASE tasks_db OWNER MyUser;
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