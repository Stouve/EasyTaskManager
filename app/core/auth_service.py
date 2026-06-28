from datetime import datetime, timezone

from app.core.user import User, RoleEnum
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

