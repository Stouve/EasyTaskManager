import pytest
from app.core.services import TaskService, InvalidTaskError
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


