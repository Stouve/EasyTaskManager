from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from datetime import datetime, timezone

from sqlalchemy.orm import relationship

from app.infrastructure.database import Base
from app.core.task import TaskStatus

class TaskModel(Base):
    """
    SQLAlchemy Task Model for Task table
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)

    status = Column(
        Enum(TaskStatus, name="taskstatus"),
        default=TaskStatus.PENDING,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

owner_id = Column(Integer, ForeignKey("users.id"),nullable=False,index=True)

owner = relationship("UserModel", back_populates="tasks")