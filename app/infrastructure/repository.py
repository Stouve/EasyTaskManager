from fontTools.ttLib.tables.S__i_l_f import table_S__i_l_f
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
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
        # reload object from database
        self.db.refresh(db_task)

        return self._to_domain(db_task)

        # --------------------------
        # CONVERSION
        # --------------------------

    def get_all_tasks(self, status: TaskStatus | None = None) -> List[Task]:
        query = self.db.query(TaskModel)

        if status:
            query = query.filter(TaskModel.status == status)

        tasks = query.all()

        return [self._to_domain(t) for t in tasks]

    def get_by_id(self,task_id:int)->Task:
        task=self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

        if task is None:
            return None
        return self._to_domain(task)

    def mark_done(self,task_id:int)->Task:
        task=self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

        if task:
            task.status = TaskStatus.DONE
            self.db.commit()

    def update_task(self, task_id:int, title: str, description: str | None)->Task:
        task=self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            return None

        task.title = title
        task.description = description

        self.db.commit()
        #reload object from database
        self.db.refresh(task)

        return task

    def delete(self, task_id:int) -> None:
        task=self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()

    def _to_domain(self, model: TaskModel) -> Task:
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            created_at=model.created_at,
        )