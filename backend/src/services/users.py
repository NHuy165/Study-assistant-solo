from pydantic import EmailStr
from sqlmodel import select

from backend.src.core.database import SessionDep
from backend.src.core.security import get_hashed_password
from backend.src.exceptions.core import ExceptionTakenInfo_409
from backend.src.models_schema.users import User, UserInput

# ----- CREATE ----- #


async def check_username_exists(session: SessionDep, username: str):
    query = select(User).where(User.username == username)
    result = (await session.execute(query)).scalars().first()

    if result is not None:
        raise ExceptionTakenInfo_409("user", "username")


async def check_email_exists(session: SessionDep, email: EmailStr):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    result = result.scalars().first()

    if result is not None:
        raise ExceptionTakenInfo_409("user", "email")


async def register_user(session: SessionDep, user_input: UserInput) -> User:
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
