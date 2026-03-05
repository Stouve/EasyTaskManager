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

class TaskService:
    """
    Handle operations and tasks persistence
    """

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

    def list_tasks(self):
        return self.repository.get_all_tasks()

    def complete_task(self, task_id: int):
        return self.repository.mark_done(task_id)

    def delete_task(self, task_id: int):
        return self.repository.delete(task_id)

