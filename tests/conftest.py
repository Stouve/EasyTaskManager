import pytest
from datetime import datetime, timezone

from core.services import TaskService, InvalidTaskError, TaskNotFoundError
from core.models import Task, TaskStatus
from infrastructure.database import init_db
from infrastructure.repository import SQLiteTaskRepository


# -------------------------
# Fake Repository (Unit tests)
# -------------------------
class FakeRepository:

    def __init__(self):
        self.tasks = {}
        self.counter = 1

    def add(self, title, description):
        now = datetime.now(timezone.utc).isoformat()
        task = Task(
            id=self.counter,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.fromisoformat(now)
        )
        self.tasks[self.counter] = task
        self.counter += 1
        return task

    def get_all_tasks(self,status:TaskStatus | None = None) -> List[Task]:
        if status is not None:
            return list(self.tasks.values())
        return [elt for elt in self.tasks.values() if elt.status == status]

    def get_by_id(self, task_id):
        return self.tasks.get(task_id)

    def mark_done(self, task_id):
        if task_id not in self.tasks:
            raise TaskNotFoundError("Not found")
        self.tasks[task_id].status = TaskStatus.DONE

    def delete(self, task_id):
        if task_id not in self.tasks:
            raise TaskNotFoundError("Not found")
        del self.tasks[task_id]

# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def service():
    """TaskService with FakeRepository(unit tests)"""
    return TaskService(FakeRepository())

@pytest.fixture
def repo(tmp_path):
    """SQLite Repository with temporary database(integration tests)"""
    db_path = tmp_path / "test.db"
    init_db(db_path)
    return SQLiteTaskRepository(db_path)