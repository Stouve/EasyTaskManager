# EasyTaskManager API

REST API to manage tasks with JWT authentication. Built with FastAPI, PostgreSQL & SQLAlchemy.

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

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migrations | Alembic |
| Auth | PyJWT + pwdlib (Argon2) |
| Dependency management | Poetry |

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

## Installation

### Prerequisites

- Python 3.13+
- PostgreSQL 18+
- Poetry

### Setup

**1 — Clone the repository**

```bash
git clone https://github.com/Stouve/EasyTaskManager
cd EasyTaskManager
poetry install
```

**2 — Set up PostgreSQL**

Fill `setup.sql` with your credentials and run:

```bash
psql -U postgres -f setup.sql
```

**3 — Configure environment variables**

Copy `.env.example` to `.env` and fill in your values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/tasks_db

JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

DEBUG=False
COOKIE_SECURE=False  # Set to True in production (HTTPS only)
```

Generate a secure JWT secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

**4 — Run database migrations**

```bash
poetry run alembic upgrade head
```

**5 — Start the server**

```bash
poetry run uvicorn app.main:app --reload
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

## API Endpoints

### Auth

| Method | Route | Description | Auth required |
|--------|-------|-------------|---------------|
| POST | `/auth/register` | Create a new account | No |
| POST | `/auth/login` | Login, returns access token (refresh token in httpOnly cookie) | No |
| POST | `/auth/refresh` | Get a new access token from refresh token cookie | No |
| POST | `/auth/logout` | Revoke refresh token | No |
| GET | `/auth/me` | Get current user info | Yes |

### Tasks

All task routes require a valid `Authorization: Bearer <access_token>` header.  
Each user can only access their own tasks.

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/tasks/` | List tasks (paginated, filterable by status) |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/{id}` | Get a task by ID |
| PUT | `/tasks/{id}` | Full update |
| PATCH | `/tasks/{id}` | Partial update |
| DELETE | `/tasks/{id}` | Delete a task |

### Query parameters for `GET /tasks/`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `status` | `pending` \| `done` | — | Filter by status |
| `page` | int | 1 | Page number |
| `page_size` | int | 10 | Items per page (max 100) |
| `sort_by` | string | `created_at` | Sort field |
| `order` | `asc` \| `desc` | `desc` | Sort order |

## Authentication Flow

```
POST /auth/register  →  account created
POST /auth/login     →  access_token (JSON) + refresh_token (httpOnly cookie)
                        ↓
Authorization: Bearer <access_token>  →  protected routes
                        ↓ (access token expires after 15 min)
POST /auth/refresh   →  new access_token (refresh token cookie sent automatically)
                        ↓
POST /auth/logout    →  refresh token revoked in DB + cookie deleted
```

**Security choices:**
- Access token: short-lived (15 min), travels in `Authorization` header
- Refresh token: long-lived (7 days), stored in httpOnly cookie (not accessible via JS), hashed in DB (SHA-256)
- Passwords hashed with Argon2 (OWASP recommended, winner of Password Hashing Competition 2015)

## Development

### Run in debug mode

Set `DEBUG=True` in `.env` to enable SQLAlchemy query logging.

### Generate a new migration after model changes

```bash
poetry run alembic revision --autogenerate -m "description of change"
poetry run alembic upgrade head
```
