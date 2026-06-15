from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.task import TaskStatus
from app.infrastructure.database import get_db
from app.infrastructure.repository import TaskRepository
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.task_schema import TaskOut, TaskCreate, TaskUpdate, TaskPatch
from typing import List
from app.core.services import TaskService, TaskNotFoundError

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

def get_task_repository(db : Session = Depends(get_db)):
    return TaskRepository(db)

def get_task_service(repo : TaskRepository = Depends(get_task_repository)):
    return TaskService(repo)

@router.get("/", response_model=PaginatedResponse[TaskOut])
def get_tasks(status:TaskStatus | None = None,
              pagination: PaginationParams = Depends(),
              service : TaskService = Depends(get_task_service)):
    return service.list_tasks(status=status,
                              page=pagination.page,
                              page_size=pagination.page_size,
                              sort_by=pagination.sort_by,
                              order=pagination.order,
                              )

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate,
                service : TaskService = Depends(get_task_service)
                ):
    return service.create_task(task.title, task.description)

@router.get("/{task_id}", response_model=TaskOut)
def get_task_by_id(task_id: int, service : TaskService = Depends(get_task_service)):

    try:
        return service.get_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int,
                task_update: TaskUpdate,
                service : TaskService = Depends(get_task_service)
                ):
    try:
        return service.update_task(task_id, task_update)

    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/{task_id}", response_model=TaskOut)
def patch_task(task_id: int,
               task_patch: TaskPatch,
               service : TaskService = Depends(get_task_service)):
    try:
        return service.patch_task(task_id, task_patch)

    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}")
def delete_task(task_id: int, service : TaskService = Depends(get_task_service)):
    try:
        service.delete_task(task_id)
        return Response(status_code=204)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
