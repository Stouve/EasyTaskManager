from core.models import Task, TaskStatus
from infrastructure.database import get_connection
from typing import List


# ==============================
# Exceptions métier
# ==============================

class TaskError(Exception):
    """Base exception for task domain"""

class TaskNotFoundError(TaskError):
    """Raised when a task does not exist."""

class InvalidTaskError(TaskError):
    """Raised when task data is invalid."""


# ==============================
# Service métier
# ==============================

class TaskService:
    # --------------------------
    # CREATE
    # --------------------------

    def __init__(self, repository):
        self.repository = repository

    def create_task(self, title: str, description : str | None = None)->Task:
        title=title.strip()

        if not title:
            raise InvalidTaskError("Task title cannot be empty")

        if description is not None:
            description=description.strip()
            if description=="":
                description=None

        return self.repository.add(title, description)

    # --------------------------
    # READ ALL
    # --------------------------
    def list_tasks(self, status:TaskStatus | None = None)->List[Task]:
        return self.repository.get_all_tasks(status)

    def get_task(self, task_id: int)->Task:

        task=self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError("Task not found")
        return task

    def complete_task(self, task_id: int):
        task=self.repository.get_by_id(task_id)

        if task.status == TaskStatus.DONE:
            return task

        self.repository.mark_done(task_id)
        task.mark_done()

        return task


    def delete_task(self, task_id: int):
        task=self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        self.repository.delete(task_id)



