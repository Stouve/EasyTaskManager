from app.core.task import Task, TaskStatus
from typing import List
from app.schemas.task_schema import TaskUpdate, TaskPatch, TaskOut
from app.schemas.pagination import PaginatedResponse
import math


# ==============================
# Exceptions métier
# ==============================

class TaskError(Exception):
    """Base exception for task domain"""

class TaskNotFoundError(TaskError):
    """Raised when a task does not exist."""

class InvalidTaskError(TaskError):
    """Raised when task data is invalid."""

class TaskAccessDeniedError(TaskError):
    """Raised when a task exists but does not belong to the requesting user"""


# ==============================
# Service métier
# ==============================

class TaskService:
    # --------------------------
    # CREATE
    # --------------------------

    def __init__(self, repository):
        self.repository = repository

    def create_task(self, title: str, owner_id: int, description : str | None = None)->Task:
        title=title.strip()

        if not title:
            raise InvalidTaskError("Task title cannot be empty")
        if len(title) > 255:
            raise InvalidTaskError("Task title cannot be longer than 255 characters")

        if description is not None:
            description=description.strip()
            if description=="":
                description=None

        return self.repository.add(title, description, owner_id)

    # --------------------------
    # READ ALL
    # --------------------------
    def list_tasks(self,
                   owner_id: int,
                   status:TaskStatus | None = None,
                   page: int = 1,
                   page_size: int = 10,
                   sort_by: str = "created_at",
                   order: str = "desc",
    )-> PaginatedResponse[TaskOut]:

        tasks, total = self.repository.get_all_tasks(owner_id=owner_id,
                                                     status=status,
                                                     page=page,
                                                     page_size=page_size,
                                                     sort_by=sort_by,
                                                     order=order,
        )

        total_pages = math.ceil(total/page_size) if total > 0 else 1

        return PaginatedResponse(items=tasks,
                                 total=total,
                                 page=page,
                                 page_size=page_size,
                                 total_pages=total_pages,
        )

    def get_task(self, task_id: int, owner_id: int)->Task:

        task=self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError("Task not found")
        self._ensure_owner(task, owner_id)
        return task

    def _ensure_owner(self, task: Task, owner_id: int)->None:
        if task.owner_id != owner_id:
            #We raise TaskNotFoundError on HTTP Caller side to avoid reveal exising task for another user
            #We raise TaskAccessDeniedError for traceability in logs
            raise TaskAccessDeniedError("Task does not belong to this user")

    def complete_task(self, task_id: int, owner_id: int) -> Task:
        task=self.get_task(task_id,owner_id)

        if task.is_complete():
            return task

        task.mark_done()
        return self.repository.update_status(task_id, TaskStatus.DONE)

    def update_task(self, task_id: int, task_update: TaskUpdate, owner_id: int) -> Task:

        task=self.repository.update_task(task_id, task_update.title, task_update.description)

        if task is None:
            raise TaskNotFoundError("Task not found")

        return task

    def patch_task(self, task_id: int, task_patch: TaskPatch, owner_id: int) -> Task:

        #Verify existence & property before writing
        self.get_task(task_id,owner_id)

        #Get data from request JSON
        update_data = task_patch.model_dump(exclude_unset=True)

        task=self.repository.patch_task(task_id,update_data)

        if task is None:
            raise TaskNotFoundError("Task not found")

        return task

    def delete_task(self, task_id: int, owner_id: int) -> Task:
        task=self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        self._ensure_owner(task, owner_id)

        self.repository.delete(task_id)



