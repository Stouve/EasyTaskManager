from typing import List

import pytest

from core.services import TaskService, InvalidTaskError, TaskNotFoundError
from core.models import Task, TaskStatus
from datetime import datetime, timezone

class FakeRepository:
    def __init__(self):
        self.tasks = {}
        self.counter = 1

    def add(self, title, description)->Task:
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

    def get_all_tasks(self,status:TaskStatus | None = None)->List[Task]:
        if status is None:
            return list(self.tasks.values())
        return [elt for elt in self.tasks.values() if elt.status == status]

    def get_by_id(self, task_id)->Task:
        return self.tasks.get(task_id)

    def mark_done(self, task_id)->Task:
        self.tasks[task_id].status = TaskStatus.DONE

    def delete(self, task_id)->Task:
        del self.tasks[task_id]

def test_create_success() -> None:
        service = TaskService(FakeRepository())
        task=service.create_task("Test",None)

        assert task.title == "Test"
        assert task.status == TaskStatus.PENDING

def test_create_test_empty_title() -> None:
        service = TaskService(FakeRepository())

        with pytest.raises(InvalidTaskError):
            service.create_task("",None)

def test_list_tasks() -> None:
        service = TaskService(FakeRepository())

        task=service.create_task("Task1",None)
        task=service.create_task("Task2",None)

        tasks=service.list_tasks()

        assert len(tasks) == 2

def test_mark_done() -> None:
        service = TaskService(FakeRepository())
        task=service.create_task("TODO",None)

        service.complete_task(task.id)

        tasks=service.list_tasks()


        assert tasks[0].status == TaskStatus.DONE

def test_delete_task() -> None:
        service = TaskService(FakeRepository())

        task=service.create_task("Task1",None)

        service.delete_task(task.id)

        tasks=service.list_tasks()

        assert len(tasks) == 0

def test_complete_nonexisting_task() -> None:
        service = TaskService(FakeRepository())

        with pytest.raises(TaskNotFoundError):
            task=service.complete_task(999)


def test_list_tasks_done() -> None:
    service = TaskService(FakeRepository())

    task = service.create_task("Task1", None)
    service.complete_task(task.id)
    task = service.create_task("Task2", None)
    task = service.create_task("Task3", None)

    tasks = service.list_tasks(TaskStatus.DONE)

    assert len(tasks) == 1

def test_list_tasks_pending() -> None:
    service = TaskService(FakeRepository())

    task = service.create_task("Task1", None)
    task = service.create_task("Task2", None)
    service.complete_task(task.id)
    task = service.create_task("Task3", None)
    service.complete_task(task.id)

    tasks = service.list_tasks(TaskStatus.PENDING)

    assert len(tasks) == 1
