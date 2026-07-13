import os

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.infrastructure.user_repository import UserRepository
from app.core.auth_service import (
    AuthService,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InactiveUserError,
    InvalidRefreshTokenError,
)
from app.schemas.user_schema import UserCreate, UserOut, UserLogin, AccessTokenResponse
from app.security.dependencies import get_current_user
from app.core.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
# En prod, COOKIE_SECURE doit être True (cookie envoyé uniquement en HTTPS).
# On le désactive par défaut en dev local en HTTP.
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "False") == "True"

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_auth_service(repo: UserRepository = Depends(get_user_repository)):
    return AuthService(repo)

