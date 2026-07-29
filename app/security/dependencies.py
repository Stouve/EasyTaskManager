from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.user import User, RoleEnum
from app.infrastructure.database import get_db
from app.infrastructure.user_repository import UserRepository
from app.security.jwt_handler import decode_token, TokenType, InvalidTokenException

# tokenUrl pointe vers la route de login : c'est uniquement utilisé pour
# générer le bouton "Authorize" dans la doc Swagger, FastAPI n'appelle
# jamais cette URL lui-même.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db),) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload=decode_token(token,expected_type=TokenType.ACCESS)
    except InvalidTokenException:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    repo= UserRepository(db)
    user = repo.get_by_id(int(user_id))

    if user is None or not user.is_active:
        raise credentials_exception
    return user

def require_role(required_role: RoleEnum):
    """
    Dependence Factory: require_role(RoleEnum.ADMIN) renvoie une
    dépendance FastAPI qui vérifie le rôle en plus de l'authentification.

    Usage : @router.get(..., dependencies=[Depends(require_role(RoleEnum.ADMIN))])
    """
    def _check_role(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role !=require_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Insufficient permissions",
                                )
        return current_user
    return _check_role



