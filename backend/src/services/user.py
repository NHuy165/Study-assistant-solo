from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.src.core.security import get_hashed_password
from backend.src.exceptions.core import ExceptionTakenInfo_409
from backend.src.models_schema.user import User, UserInput

# ----- CREATE ----- #


async def check_username_exists(session: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    user = (await session.execute(query)).scalars().first()

    if user is not None:
        raise ExceptionTakenInfo_409("user", "username")


async def check_email_exists(session: AsyncSession, email: EmailStr):
    query = select(User).where(User.email == email)
    user = (await session.execute(query)).scalars().first()

    if user is not None:
        raise ExceptionTakenInfo_409("user", "email")


async def register_user(session: AsyncSession, user_input: UserInput) -> User:
    await check_username_exists(session, user_input.username)
    await check_email_exists(session, user_input.email)

    user = User.model_validate(
        user_input.model_dump(),
        update={"hashed_password": get_hashed_password(user_input.password)},
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
