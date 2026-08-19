import pytest
from app.core.services import TaskService, InvalidTaskError, TaskAccessDeniedError, TaskNotFoundError
from app.infrastructure.repository import TaskRepository
from tests.conftest import db_session

# ==============================
# Validation Tests (no real DB needed)
# ==============================

def test_create_task_with_empty_title_raises_error():
    service=TaskService(repository=None)

    with pytest.raises(InvalidTaskError):
        service.create_task(title="", owner_id=1)

def test_create_task_with_title_too_long_raises_error():
    service=TaskService(repository=None)
    too_long="a"*256

    with pytest.raises(InvalidTaskError):
        service.create_task(title=too_long, owner_id=1)

# ==============================
# Tests with DB using conftest fixture
# ==============================

def test_create_task_success(db_session):
    repo = TaskRepository(db_session)
    service=TaskService(repository=repo)

    task = service.create_task(title="test_task", owner_id=1, description="test_task")

    assert task.id is not None
    assert task.title == "test_task"
    assert task.description == "test_task"
    assert task.owner_id == 1

def test_get_task_returns_task_when_owner_matches(db_session):
    repo = TaskRepository(db_session)
    service=TaskService(repository=repo)

    created_task=service.create_task(title="test_task", owner_id=1, description="test_task")

    fetched_task = service.get_task(task_id=1, owner_id=1)

    assert fetched_task.id == created_task.id
    assert fetched_task.title == created_task.title

def test_get_task_raises_access_denied_when_owner_mismatch(db_session):
    repo = TaskRepository(db_session)
    service=TaskService(repository=repo)

    created_task=service.create_task(title="test_task", owner_id=1, description="test_task")

    with pytest.raises(TaskAccessDeniedError):
        fetched_task = service.get_task(task_id=1, owner_id=2)

def test_get_task_raises_not_found_when_task_does_not_exist(db_session):
    repo = TaskRepository(db_session)
    service=TaskService(repository=repo)

    with pytest.raises(TaskNotFoundError):
        fetched_task = service.get_task(task_id=999, owner_id=1)