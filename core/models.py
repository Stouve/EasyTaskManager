from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"

@dataclass
class Task(slots=True):
    """
    This represents a task

    Attributes:
        id(int) : unique identifier of the task
        title (str) : title of the task
        description (str) : description of the task
        status (str) : status of the task
        created_at (datetime) : date and time of the task
    """

    id: int | None
    title: str
    status : TaskStatus
    created_at: datetime
    description: str | None = None

    def mark_done(self) -> None:

        self.status = TaskStatus.DONE

    def mark_pending(self) -> None:
        """
        Marks the task as pending
        """
        self.status = TaskStatus.PENDING

    def is_complete(self) -> bool:
        return self.status == TaskStatus.DONE


"""
    old check function
    def __post_init__(self) -> None:

        Post initialization Validiation
        
        if not isinstance(self.id, int):
            raise TypeError("Task id must be an integer")
        if self.id < 0:
            raise ValueError("Task id must be greater than 0")
        if not isinstance(self.title, str):
            raise TypeError("Task title must be an string")
        if not self.title.strip():
            raise ValueError("Task title must not be empty")
        if not isinstance(self.done, bool):
            raise TypeError("Task done must be a boolean")
"""

