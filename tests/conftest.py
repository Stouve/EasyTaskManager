import pytest
from datetime import datetime

from core.services import TaskService
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
        task = Task(
            id=self.counter,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.utcnow(),
        )
        self.tasks[self.counter] = task
        self.counter += 1
        return task

    def get_all(self):
        return list(self.tasks.values())

    def get_by_id(self, task_id):
        return self.tasks.get(task_id)

    def mark_done(self, task_id):
        if task_id not in self.tasks:
            raise Exception("Not found")
        self.tasks[task_id].status = TaskStatus.DONE

    def delete(self, task_id):
        if task_id not in self.tasks:
            raise Exception("Not found")
        del self.tasks[task_id]

