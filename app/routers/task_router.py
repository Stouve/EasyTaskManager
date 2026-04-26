from fastapi import APIRouter, Depends
from app.infrastructure.database import get_db
from app.infrastructure.repository import TaskRepository
from app.schemas.task_schema import TaskOut
from typing import List

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

def get_task_repository(db=Depends(get_db)):
    return TaskRepository(db)

@router.get("/", response_model=List[TaskOut])
def get_tasks(repo : TaskRepository = Depends(get_task_repository)):
    return repo.get_all_tasks()

