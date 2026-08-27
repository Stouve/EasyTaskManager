import pytest
import httpx

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.infrastructure.database import Base, get_db
from app.infrastructure import models
from app.infrastructure.user_repository import UserRepository
from app.core.auth_service import AuthService

from app.main import app

# --------------------------
# test Engine DB (once for test session)
# --------------------------
@pytest.fixture(scope="session")
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
async def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    #creates bridge to call requests on memory not from network, no need to run server for tests
    transport = httpx.ASGITransport(app=app)
    #creates http test client
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

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

@pytest.fixture(scope="function")
async def auth_headers(client, test_user):
    """
    Login via HTTP API(not via service) to get real JWT token
    returns ready to inject headers in protected request
    """
    response = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "strongpassword123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}