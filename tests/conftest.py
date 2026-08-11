import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.infrastructure.database import Base, get_db
from app.infrastructure import models
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
