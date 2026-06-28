from datetime import datetime, timezone

from sqlalchemy.sql.functions import user

from app.core.user import User, RoleEnum
from app.infrastructure.user_repository import UserRepository
from app.security.password_hasher import hash_password, verify_password
from app.security.jwt_handler import (
    create_access_token,
    create_refresh_token,
    decode_token,
    TokenType,
    InvalidTokenException,
)

# ==============================
# Exceptions
# ==============================

class AuthError(Exception):
    """Base exception for auth domain"""

class EmailAlreadyExists(AuthError):
    """Raised when email already exists"""

class InvalidCredentials(AuthError):
    """Raised when invalid credentials are given"""

class InactiveUserError(AuthError):
    """Raised when inactive users tries to authenticate"""

class InvalidRefreshToken(AuthError):
    """Raised when refresh token is invalid, expired, revoked, or unknown"""

class AuthService:

    def __init__(self, user_repository: UserRepository) -> User:
        self.user_repository = user_repository

    def register(self,email:str, password:str)->User:
        email=email.strip().lower()

        existing = self.user_repository.get_by_email(email)
        if existing is not None:
            raise EmailAlreadyExists("Email already exists")

        hashed_password = hash_password(password)

        return(self.user_repository.add(email, hashed_password, role=RoleEnum.USER))