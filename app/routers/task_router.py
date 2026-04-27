from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import task
from app.infrastructure.database import get_db
from app.infrastructure.repository import TaskRepository
from app.schemas.task_schema import TaskOut, TaskCreate
from typing import List
from app.core.services import Task, TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

def get_task_repository(db : Session = Depends(get_db)):
    return TaskRepository(db)

def get_task_service(repo : TaskRepository = Depends(get_task_repository)):
    return TaskService(repo)

@router.get("/", response_model=List[TaskOut])
def get_tasks(service : TaskService = Depends(get_task_service)):
    return service.list_tasks()

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate,
                service : TaskService = Depends(get_task_service)
                ):
    return service.create_task(task.title, task.description)

@router.get("/{task_id}", response_model=TaskOut)
def get_task_by_id(task_id: int, service : TaskService = Depends(get_task_service)):
    return service.get_task(task_id)

@router.delete("/{task_id}")
def delete_task(task_id: int, service : TaskService = Depends(get_task_service)):
    return service.delete_task(task_id)
