from pydantic import EmailStr
from sqlmodel import select

from backend.src.core.database import SessionDep
from backend.src.core.security import create_token, verify_password
from backend.src.exceptions.core import ExceptionAuthentication_401
from backend.src.models_schema.auth import Token
from backend.src.models_schema.users import User


async def authenticate_user(
    session: SessionDep, email: EmailStr, password: str
) -> User:
    query = select(User).where(User.email == email)
    user = (await session.execute(query)).scalars().first()

    if user is None:
        raise ExceptionAuthentication_401()

    if not verify_password(password, user.hashed_password):
        raise ExceptionAuthentication_401()

    return user


async def login_for_token(session: SessionDep, email: EmailStr, password: str) -> Token:
    user = await authenticate_user(session, email, password)

    data = {"sub": str(user.id)}
    token_str = create_token(data)

    return Token(access_token=token_str, token_type="bearer")
