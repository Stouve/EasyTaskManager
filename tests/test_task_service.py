import pytest
from app.core.services import TaskService, InvalidTaskError

def test_create_task_with_empty_title_raises_error():
    service=TaskService(repository=None)

    with pytest.raises(InvalidTaskError):
        service.create_task(title="", owner_id=1)