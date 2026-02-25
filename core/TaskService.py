import json
from pathlib import Path
from typing import List, Optional

from core.models import Task


class TaskManager():
    """
    Handle operations and tasks persistence
    """

    def __init__(self, repository):
        self.repository = repository

    def createTask(self, title: str, description : str | None):
        if not title:
            raise ValueError("Task title cannot be empty")
        return self.repository.add(title, description)

    def listTasks(self):
        return self.repository.get_all_tasks()

    def completeTask(self, task_id: int):
        return self.repository.mark_done(task_id)

    def deleteTask(self, task_id: int):
        return self.repository.delete(task_id)