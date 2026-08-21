import pytest

from app.security.password_hasher import verify_password
from app.core.user import RoleEnum
from app.core.auth_service import EmailAlreadyExistsError, InvalidCredentialsError, InactiveUserError

def test_register_creates_user(auth_service):

    #Arrange

    email="test@example.com"
    password="strongpassword123"

    #Act
    user_created=auth_service.register(email,password)

    assert user_created.id is not None
    assert user_created.email==email
    assert verify_password(password, user_created.hashed_password) is True
    assert user_created.hashed_password != password #check that password is hashed and not plain
    assert user_created.role==RoleEnum.USER
    assert user_created.is_active is True


def test_register_with_existing_email_raises_error(auth_service):

    email = "test@example.com"
    password = "strongpassword123"
    user_created=auth_service.register(email,password)

    with pytest.raises(EmailAlreadyExistsError):
        user_created = auth_service.register(email, "anotherpassword456")

def test_authenticate_with_wrong_password_raises_error(auth_service):
    email = "test@example.com"
    password = "strongpassword123"
    user_created = auth_service.register(email, password)

    with pytest.raises(InvalidCredentialsError):
        user=auth_service.authenticate(email, "wrong_password")

def test_authenticate_with_wrong_user_raises_error(auth_service):
    email = "test@example.com"
    password = "strongpassword123"
    user_created = auth_service.register(email, password)

    with pytest.raises(InvalidCredentialsError):
        user=auth_service.authenticate("fake@example.com", password)
