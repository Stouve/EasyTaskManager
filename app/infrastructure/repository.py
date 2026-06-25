from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Optional
from app.infrastructure.db_models import TaskModel
from app.core.task import Task, TaskStatus
from app.schemas.task_schema import TaskUpdate
from sqlalchemy import asc, desc

ALLOWED_SORT_FIELDS={"id","title","created_at","status"}

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

    def get_all_tasks(self,
                      status: TaskStatus | None = None,
                      page: int = 1,
                      page_size: int = 10,
                      sort_by: str = "created_at",
                      order : str = "desc",
                      ) -> tuple[List[Task], int]:

        #If required field is not in allowed values we force created_at as default
        if sort_by not in ALLOWED_SORT_FIELDS:
            sort_by = "created_at"

        query = self.db.query(TaskModel)

        if status:
            query = query.filter(TaskModel.status == status)

        #check total before to calculate total pages from service
        total= query.count()

        sort_column = getattr(TaskModel, sort_by)

        query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))

        #offset : how elements are ignored before reading
        offset = (page-1) * page_size

        tasks = query.offset(offset).limit(page_size).all()

        return [self._to_domain(t) for t in tasks], total



    def get_by_id(self,task_id:int)-> Task | None:
        task=self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

        if task is None:
            return None
        return self._to_domain(task)

    def update_task(self, task_id:int, title: str, description: str | None)-> Task | None:
        task_md=self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task_md:
            return None

        task_md.title = title
        task_md.description = description

        return self.save(task_md)

    def patch_task(self, task_id:int, update_data:dict) -> Task | None:
        task_md=self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

        if not task_md:
            return None

        for field,value in update_data.items():
            setattr(task_md,field,value)

        return self.save(task_md)

    def update_status(self, task_id:int, status: TaskStatus)-> Task | None:
        task_md=self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task_md:
            return None

        task_md.status = status
        return self.save(task_md)

    def save(self, task_model:TaskModel)->Task:

        self.db.commit()
        #Reload object from database
        self.db.refresh(task_model)
        return self._to_domain(task_model)

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