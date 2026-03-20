from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.infrastructure.db_models import TaskModel
from app.core.task import Task, TaskStatus

class TaskRepository:

    def __init__(self, db: Session):
        self.db = db

    # --------------------------
    # CREATE
    # --------------------------
    def add(self, title: str, description: str | None) -> Task:
        db_task=TaskModel(
            title=title,
            description=description,
        )

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        return self._to_domain(db_task)

        # --------------------------
        # CONVERSION
        # --------------------------

    def _to_domain(self, model: TaskModel) -> Task:
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            created_at=datetime.fromisoformat(model.created_at),
        )