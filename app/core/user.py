from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass(slots=True)
class User:
    """
    This represents a User

    Attributes:
        id(int) : unique identifier of the user
        email (str) : email of the user(used as id for connection)
        hashed_password (str) : hashed password of the user
        role (RoleEnum) : role of the user(user/admin)
        created_at (datetime) : date and time when the user was created
        is_active (bool) : whether the user is active or not
    """
    id: int | None
    email: str
    hashed_password: str
    role: RoleEnum
    created_at: datetime
    is_active: bool = True

    def isAdmin(self) -> bool:
        return self.role == RoleEnum.ADMIN