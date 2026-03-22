from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from backend.src.core.config import settings

password_hasher = PasswordHash.recommended()


def get_hashed_password(password: str):
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hasher.verify(password, hashed_password)


def create_token(data: dict) -> str:
    data = data.copy()

    now = datetime.now(timezone.utc)

    data.update({"iat": now, "exp": now + timedelta(hours=settings.TOKEN_EXPIRY_HOURS)})

    token = jwt.encode(
        payload=data,
        key=settings.PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token
