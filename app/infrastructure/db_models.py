from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime, timezone
from app.infrastructure.database import Base
from app.core.task import TaskStatus

class TaskModel(Base):
    """
    Modèle SQLAlchemy représentant la table 'tasks'
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
