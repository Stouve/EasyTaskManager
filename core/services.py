from core.models import Task
from infrastructure.database import get_connection

class TaskService():
    """
    Handle operations and tasks persistence
    """

    def __init__(self, repository):
        self.repository = repository

    def create_task(self, title: str, description : str | None):
        if not title:
            raise ValueError("Task title cannot be empty")
        return self.repository.add(title, description)

    def list_tasks(self):
        return self.repository.get_all_tasks()

    def complete_task(self, task_id: int):
        return self.repository.mark_done(task_id)

    def delete_task(self, task_id: int):
        return self.repository.delete(task_id)

