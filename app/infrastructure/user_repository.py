import hashlib

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.core.user import User, RoleEnum
from app.infrastructure.user_models import UserModel, RefreshTokenModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # --------------------------
    # USERS
    # --------------------------

    def add(self, email: str, hashed_password: str, role: RoleEnum = RoleEnum.USER) -> User:
        db_user = UserModel(
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
        self.db.add(db_user)
        self.db.commit()
        #reload object from database
        self.db.refresh(db_user)

        return self._to_domain(db_user)

    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
        )