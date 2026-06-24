from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

from app.core.user import RoleEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AccessTokenResponse(BaseModel):
    """
    Response from login/refresh, only access token is exposed in JSON body response.
    Refresh token is in cookie httpOnly on server side, never readable from client side
    """
    access_token: str
    token_type: "bearer"
