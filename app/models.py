from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base
from datetime import datetime, timezone
import enum

class TaskStatusDB(str, enum.Enum):
    PENDING = "pending"
    DONE = "done"

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatusDB), default=TaskStatusDB.PENDING)
    created_at = Column(DateTime, defaut=datetime.now(timezone.utc).isoformat())
