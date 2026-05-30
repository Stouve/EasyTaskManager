from datetime import datetime

from pydantic import BaseModel
from typing import Optional

from app.core.task import TaskStatus


#For DATA IN (POST/PUT)
class TaskCreate(BaseModel):
    title:str
    description: Optional[str] = None


#For DATA OUT (GET)
class TaskOut(BaseModel):
    id: int
    title: str
    status: TaskStatus
    created_at: datetime
    description: Optional[str] = None

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

