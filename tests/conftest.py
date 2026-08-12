import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.infrastructure.database import Base, get_db
from app.infrastructure import models
from app.infrastructure.user_repository import UserRepository
from app.core.auth_service import AuthService

from app.main import app

# --------------------------
# test Engine DB (once for test session)
# --------------------------
@pytest.fixture
def engine():
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}, # SQLite doesn't allow mutlithread by default
        poolclass=StaticPool, # keep same connection in memory between calls
    )

@pytest.fixture(scope="session", autouse=True)
def create_tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

# --------------------------
# isolated session per test (auto rollback)
# --------------------------
@pytest.fixture(scope="function")
def db_session(engine) -> Session:
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()  # annule tout ce que le test a écrit
    connection.close()


# --------------------------
# HTTP test client, with injected test DB
# --------------------------
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()  # clean after test

@pytest.fixture(scope="function")
def auth_service(db_session) -> AuthService:
    repo = UserRepository(db_session)
    return AuthService(repo)

@pytest.fixture(scope="function")
def test_user(auth_service):
    """Create test user directly from service(not via HTTP)"""
    user = auth_service.register(email="test@example.com", password="strongpassword123")
    return user