import pytest

from app.infrastructure.user_repository import UserRepository
from app.security.password_hasher import verify_password
from app.core.user import RoleEnum

def test_register_creates_user(auth_service):

    #Arrange

    email="test@example.com"
    password="strongpassword123"

    #Act
    user_created=auth_service.register(email,password)

    assert user_created.id is not None
    assert user_created.email==email
    assert verify_password(password, user_created.hashed_password) is True
    assert user_created.role==RoleEnum.USER
    assert user_created.is_active is True
    assert user_created.hashed_password != password

