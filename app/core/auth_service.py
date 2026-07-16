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

class EmailAlreadyExistsError(AuthError):
    """Raised when email already exists"""

class InvalidCredentialsError(AuthError):
    """Raised when invalid credentials are given"""

class InactiveUserError(AuthError):
    """Raised when inactive users tries to authenticate"""

class InvalidRefreshTokenError(AuthError):
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

    def authenticate(self, email:str, password:str)->User:
        email=email.strip().lower()

        user=self.user_repository.get_by_email(email)

        if user is None:
            raise InvalidCredentials("Invalid Email or password")
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentials("Invalid Email or password")
        if not user.is_active:
            raise InactiveUserError("Inactive user")
        return user

# ==============================
# TOKENS
# ==============================

def issue_tokens(self, user: User) -> tuple[str, str, datetime]:
    """
    Generate access & refresh tokens for user, store hashed refresh token in db,
    returns access_token, refresh_token, refresh_expires_at
    """
    access_token=create_access_token(subject=str(user.id), role=user.role.value)
    refresh_token, expires_at=create_refresh_token(subject=str(user.id), role=user.role.value)

    self.user_repository.store_refresh_token(user.id,refresh_token,expires_at)

    return access_token, refresh_token, expires_at

def refresh_access_token(self, raw_refresh_token:str)->str:
    """
    verify refresh token(signature, type, validity) and generates new access token, refresh token is not renewed
    """
    try:
        payload=decode_token(raw_refresh_token,expected_type=TokenType.REFRESH)
    except InvalidTokenException:
        raise InvalidRefreshToken("Refresh token is invalid or expired")

    #get token from DB
    db_token=self.user_repository.get_valid_refresh_token(raw_refresh_token)
    if db_token is None:
        raise InvalidRefreshToken("Refresh token is invalid or expired")

    #Check if token is not expired
    if db_token.expires_at < datetime.now(timezone.utc):
        raise InvalidRefreshToken("Refresh token is expired")

    user_id=int(payload["sub"])
    user = self.user_repository.get_by_id(user_id)

    if user is None or not user.is_active:
        raise InvalidRefreshToken("User not found or inactive")

    return(create_access_token(subject=str(user.id), role=user.role.value))

def logout(self,raw_refresh_token)->None:
    self.user_repository.revoke_refresh_token(raw_refresh_token)
