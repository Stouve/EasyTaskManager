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
        #Conversion to object type user from db
        return self._to_domain(db_user)

    def get_by_email(self, email: str) -> Optional[User]:

        user = self.db.query(UserModel).filter(UserModel.email == email).first()

        if user is None:
            return None
        return self._to_domain(user)

    def get_by_id(self, user_id: int) -> Optional[User]:

        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            return None
        return self._to_domain(user)


    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
        )

    # --------------------------
    # REFRESH TOKENS
    # --------------------------

    @staticmethod
    def _hash_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

    def store_refresh_token(self, user_id: int, raw_token:str, expires_at: datetime) -> Optional[RefreshTokenModel]:
        db_token=RefreshTokenModel(
            token_hash=self._hash_token(raw_token),
            user_id=user_id,
            expires_at=expires_at,
        )
        self.db.add(db_token)
        self.db.commit()

def get_valid_refresh_token(self,raw_token:str) -> Optional[RefreshTokenModel]:

   token_hash=self._hash_token(raw_token)
   return(
       self.db.query(RefreshTokenModel).filter(
           RefreshTokenModel.token_hash == token_hash,
           RefreshTokenModel.revoked.is_(False)
       ).first()
   )

def revoke_refresh_token(self, raw_token:str) -> None:
    token_hash=self._hash_token(raw_token)
    db_token=self.db.query(RefreshTokenModel).filter(RefreshTokenModel.token_hash == token_hash).first()

    if db_token:
        db_token.revoked = True
        self.db.commit()

def revoke_all_refresh_tokens_for_user(self, user_id:int) -> None:

    self.db.query(RefreshTokenModel).filter(RefreshTokenModel.user_id == user_id,
                                            RefreshTokenModel.revoked.is_(False)
                                            ).update({"revoked": True})
    self.db.commit()






