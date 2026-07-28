from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean, column
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.infrastructure.database import Base
from app.core.user import RoleEnum


class UserModel(Base):
    """
    SQLAlchemy User Model for User table
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)

    role = Column(
        Enum(RoleEnum, name="roleenum"),
        default=RoleEnum.USER,
        nullable=False
    )

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    tasks = relationship("TaskModel", back_populates="owner", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshTokenModel", back_populates="user",cascade="all, delete-orphan")

class RefreshTokenModel(Base):
    """
    SQLAlchemy RefreshToken Model for RefreshToken table
    we never store raw token but his sha256 hash
    """
    __tablename__ = "refresh_token"
    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(255), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user=relationship("UserModel", back_populates="refresh_token")
