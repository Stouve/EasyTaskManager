from typing import List

import pytest

from core.services import TaskService, InvalidTaskError
from core.models import Task, TaskStatus
from datetime import datetime, timezone

class FakeRepository:
    def __init__(self):
        self.tasks = {}
        self.counter = 1

    def add(self, title, description)->Task:
        now = datetime.now(timezone.utc).isoformat()
        task = Task(
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.fromisoformat(now)
        )
        self.tasks[self.counter] = task
        self.counter += 1
        return task

def get_all(self)->List[Task]:
    return list(self.tasks.values())

def get_by_id(self, task_id)->Task:
    return self.tasks.get(task_id)

def mark_done(self, task_id)->Task:
    self.tasks[task_id].status = TaskStatus.DONE

def delete(self, task_id)->Task:
    del self.tasks[task_id]
