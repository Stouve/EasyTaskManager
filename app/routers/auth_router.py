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


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_TOKEN_EXPIRE_DAYS,
        value=refresh_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",#CSRF base protection to avoid cookie to be sent on cross site requests
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/auth", # Cookie sent on /auth routes only
    )

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, service : AuthService = Depends(get_auth_service)):
    try:
        return service.register(user_create.email, user_create.password)
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.post("/login", response_model=AccessTokenResponse)
def login(credentials: UserLogin, response: Response, service : AuthService = Depends(get_auth_service)):
    try:
        user=service.authenticate(credentials.email, credentials.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    except InactiveUserError:
        raise HTTPException(status_code=403, detail="Inactive user")

    access_token, refresh_token, _ = service.issue_tokens(user)
    _set_refresh_cookie(response, refresh_token)

    return AccessTokenResponse(access_token=access_token)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
        request: Request,
        response: Response,
        service : AuthService = Depends(get_auth_service),
):
    raw_refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if raw_refresh_token:
        service.logout(raw_refresh_token)
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/auth")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user