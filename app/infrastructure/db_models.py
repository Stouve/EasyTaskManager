from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime, timezone
from app.infrastructure.database import Base
from app.core.task import TaskStatus  # On utilise l'enum métier

class TaskModel(Base):
    """
    Modèle SQLAlchemy représentant la table 'tasks'
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc).isoformat(), nullable=False)