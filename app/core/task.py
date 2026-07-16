from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"


@dataclass(slots=True)
class Task:
    """
    This represents a task

    Attributes:
        id(int) : unique identifier of the task
        title (str) : title of the task
        description (str) : description of the task
        status (str) : status of the task
        created_at (datetime) : date and time of the task
        owner_id(int) : id of the owner of the task
    """

    id: int | None
    title: str
    status: TaskStatus
    created_at: datetime
    owner_id: int
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
