from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.task import TaskStatus
from app.infrastructure.database import get_db
from app.infrastructure.repository import TaskRepository
from app.schemas.task_schema import TaskOut, TaskCreate, TaskUpdate
from typing import List
from app.core.services import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

def get_task_repository(db : Session = Depends(get_db)):
    return TaskRepository(db)

def get_task_service(repo : TaskRepository = Depends(get_task_repository)):
    return TaskService(repo)

@router.get("/", response_model=List[TaskOut])
def get_tasks(status:TaskStatus | None = None, service : TaskService = Depends(get_task_service)):
    return service.list_tasks(status)

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate,
                service : TaskService = Depends(get_task_service)
                ):
    return service.create_task(task.title, task.description)

@router.get("/{task_id}", response_model=TaskOut)
def get_task_by_id(task_id: int, service : TaskService = Depends(get_task_service)):
    return service.get_task(task_id)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int,
                task: TaskUpdate,
                service : TaskService = Depends(get_task_service)
                ):
    try:
        return service.update_task(task_id, task.title, task.description)

    except ValueError:
        raise HTTPException(404)


@router.delete("/{task_id}")
def delete_task(task_id: int, service : TaskService = Depends(get_task_service)):
    return service.delete_task(task_id)
