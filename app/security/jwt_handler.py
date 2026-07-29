import os
from datetime import datetime, timedelta, timezone
from enum import Enum

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic.color import parse_tuple

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set in environment variables")

class TokenType(str, Enum):
    ACCESS = "access",
    REFRESH = "refresh"

class InvalidTokenException(Exception):
    """Raised when the token is invalid"""

def create_access_token(subject: str, role: str) -> str:
    return _create_token(
        subject=subject,
        role=role,
        token_type=TokenType.ACCESS,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

def create_refresh_token(subject: str, role: str) -> tuple[str, datetime]:
    """
    return signed token & expiration date
    """
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token = _create_token(
        subject=subject,
        role=role,
        token_type=TokenType.REFRESH,
        expires_at=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return token, expires_at

def _create_token(subject: str, role: str, token_type: TokenType, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject, #user id
        "role": role,
        "type": token_type.value,
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="JWT_ALGORITHM")

def decode_token(token: str, expected_type: TokenType) -> dict:
    """
    Decode and verify token, token type
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise InvalidTokenException("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenException("Invalid token")

    if payload["type"] != expected_type.value:
        raise InvalidTokenException("Unexpected token type")

    return payload
