# EasyTaskManager API

A REST API for task management built with FastAPI and PostgreSQL. The project includes JWT authentication and role-based access control. The application is organized into separate layers for API routes, business logic, and database access.
## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.13 |
| API framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation | Pydantic |
| Authentication | PyJWT |
| Password hashing | pwdlib (Argon2) |
| Dependency management | Poetry |
| Containerization | Docker & Docker Compose |


## Getting Started

### Run with Docker

**Prerequisites:** Docker Desktop installed and running.

Clone the repository and start the application:

```bash
git clone https://github.com/Stouve/EasyTaskManager.git
cd EasyTaskManager
docker compose up --build
```

Docker Compose starts the PostgreSQL database and the API. On initial setup, the application image is built and the database migrations are applied.

Once the application is running, the interactive API documentation is available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

To stop the application:

```bash
docker compose down
```

To also remove the database volume and its stored data:

```bash
docker compose down -v
```

> The credentials configured in `docker-compose.yml` are for local development only.

### Run locally

**Prerequisites:**
- Python 3.13+
- PostgreSQL 18+
- Poetry

**1. Install dependencies**

```bash
git clone https://github.com/Stouve/EasyTaskManager.git
cd EasyTaskManager
poetry install
```

**2. Configure PostgreSQL**

Set up a PostgreSQL database and user using `setup.sql`, adapting the script to your local configuration. Run it with:

```bash
psql -U postgres -f setup.sql
```

**3. Configure environment variables**

Copy `.env.example` to `.env` and update the values for your environment.

```dotenv
DATABASE_URL=postgresql://user:password@localhost:5432/tasks_db

JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

DEBUG=False
COOKIE_SECURE=False
```

Generate a secret key for local development:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Set `COOKIE_SECURE=True` when deploying behind HTTPS. Use appropriate secrets and configuration for any production deployment.

**4. Apply database migrations**

```bash
poetry run alembic upgrade head
```

**5. Start the API**

```bash
poetry run uvicorn app.main:app --reload
```

API available at `http://localhost:8000`  
API documentation is available at http://localhost:8000/docs.

## Features

- **Task management:** Create, retrieve, update, and delete tasks.
- **Authentication:** User registration and login using JWT access and refresh tokens.
- **Role-based access control:** Separate permissions for users and administrators.
- **User isolation:** Users can access only their own tasks.
- **Pagination and sorting:** Support for paginated task listings.
- **Token revocation:** Refresh tokens are stored server-side and can be revoked.
- **Password security:** Passwords are hashed using Argon2.
- **Database migrations:** Schema changes are managed with Alembic.

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
