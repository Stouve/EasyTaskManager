import pytest

from core.services import TaskService, InvalidTaskError, TaskNotFoundError
from core.models import Task, TaskStatus

from tests.conftest import FakeRepository

def test_create_task(service):
    task=service.create_task("Test",None)
    assert task.title == "Test"
    assert task.status == TaskStatus.PENDING

def test_empty_title(service):
    with pytest.raises(InvalidTaskError):
        service.create_task("", None)

def test_title_only_spaces(service):
    with pytest.raises(InvalidTaskError):
        service.create_task("    ",None)

def test_list_tasks(service):
    service.create_task("Task1",None)
    service.create_task("Task2",None)

    tasks=service.list_tasks()
    assert len(tasks) == 2

def test_filter_tasks(service):
    t1=service.create_task("Task1",None)
    t2=service.create_task("Task2",None)

    service.complete_task(t2.id)

    done_tasks=service.list_tasks(TaskStatus.DONE)
    assert len(done_tasks) == 1
    assert done_tasks[0].status == TaskStatus.DONE

def complete_task(service):
    t1=service.create_task("Task1",None)

    updated=service.list_tasks()[0]

    assert updated.status == TaskStatus.DONE

def test_delete_task(service):
    t1=service.create_task("Task1",None)
    service.delete_task(t1.id)

    tasks=service.list_tasks()

    assert len(tasks) == 0

def test_complete_nonexisting_task(service):
    with pytest.raises(TaskNotFoundError):
        service.complete_task(999)

def test_list_tasks_done(service):

    task = service.create_task("Task1", None)
    service.complete_task(task.id)
    service.create_task("Task2", None)
    service.create_task("Task3", None)

    tasks = service.list_tasks(TaskStatus.DONE)

    assert len(tasks) == 1

def test_list_tasks_pending(service) -> None:

    service.create_task("Task1", None)
    task = service.create_task("Task2", None)
    service.complete_task(task.id)
    task = service.create_task("Task3", None)
    service.complete_task(task.id)

    tasks = service.list_tasks(TaskStatus.PENDING)

    assert len(tasks) == 1

