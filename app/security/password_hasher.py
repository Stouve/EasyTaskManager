from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()

def hash_password(plain_password: str) -> str:
    """
    Hash password using password hashing algorithm Argon2
    :param plain_password:
    :return:
    """
    return _password_hash.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:

    return _password_hash.verify(plain_password, hashed_password)