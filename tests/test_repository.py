from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import TaskRepository
from app.core.task import TaskStatus


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

