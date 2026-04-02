import pytest
from sqlalchemy import create_engine

from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal, Base, engine
from app.infrastructure.repository import TaskRepository
from app.core.task import TaskStatus

# Engine once
@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

#Tables once
@pytest.fixture(scope="session", autouse=True)
def create_tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

#Session, one per test
@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=engine)
    yield session

    session.close()
    transaction.rollback()
    connection.close()


def test_create_task():
    db = SessionLocal()
    repo = TaskRepository(db)

    task = repo.add("Test task", "description")

    assert task is not None
    assert task.title == "Test task"

    db.close()

def test_get_tasks():
    db = SessionLocal()
    repo = TaskRepository(db)

    tasks=repo.get_all_tasks()
    assert isinstance(tasks, list)

    db.close()

def test_filter_tasks():
    db = SessionLocal()
    repo = TaskRepository(db)

    tasks = repo.get_all_tasks(TaskStatus.PENDING)

    for t in tasks:
        assert t.status == TaskStatus.PENDING

    db.close()

