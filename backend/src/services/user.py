from datetime import datetime, timedelta, timezone

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from backend.src.core.security import get_hashed_password, verify_password
from backend.src.exceptions.core import (
    ExceptionAuthentication_401,
    ExceptionTakenInfo_409,
)
from backend.src.models_schema.user.check_in import CheckIn
from backend.src.models_schema.user.user import (
    User,
    UserInput,
    UserPasswordChange,
    UserUpdate,
)

# ----- CREATE ----- #


async def check_email_exists(session: AsyncSession, email: EmailStr):
    query = select(User).where(User.email == email)
    user = (await session.execute(query)).scalars().first()

    if user is not None:
        raise ExceptionTakenInfo_409("user", "email")


async def register_user(session: AsyncSession, user_input: UserInput) -> User:
    await check_email_exists(session, user_input.email)
    await session.commit()

    user = User.model_validate(
        user_input.model_dump(),
        update={"hashed_password": get_hashed_password(user_input.password)},
    )

    session.add(user)
    await session.commit()
    # await session.refresh(user)

    return user


async def check_in(user: User, session: AsyncSession) -> tuple[User, CheckIn] | None:
    query = (
        select(CheckIn)
        .where(CheckIn.user_id == user.id)
        .order_by(col(CheckIn.time).desc())
        .limit(1)
    )
    last_check_in = (await session.execute(query)).scalars().first()

    today = datetime.now(timezone.utc).date()

    # If user has never logged in or didn't log in today
    if last_check_in is None or last_check_in.time < today:
        # If user has never logged in
        if last_check_in is None:
            user.login_streak = 1
            user.longest_login_streak = 1
        else:
            time_between = today - last_check_in.time

            # If user last logged in yesterday
            if time_between == timedelta(days=1):
                user.login_streak += 1
                if user.login_streak > user.longest_login_streak:
                    user.longest_login_streak = user.login_streak

            # If user didn't log in yesterday
            elif time_between > timedelta(days=1):
                user.login_streak = 1

        new_check_in = CheckIn(
            time=today,
            user=user,
        )

        session.add(new_check_in)
        await session.commit()

        return user, new_check_in


# ----- READ ----- #


async def read_user(user: User) -> User:
    return user


# ----- UPDATE ----- #


async def update_user(
    user: User, session: AsyncSession, user_update: UserUpdate
) -> User:
    update_contents = user_update.model_dump(exclude_unset=True)

    if (
        update_contents.get("email", None)
        and update_contents.get("email", None) != user.email
    ):
        await check_email_exists(session, update_contents["email"])

    user.sqlmodel_update(update_contents)

    await session.commit()
    # await session.refresh(user)
    return user


async def update_password(
    user: User, session: AsyncSession, password_change: UserPasswordChange
) -> None:
    if not verify_password(password_change.old_password, user.hashed_password):
        raise ExceptionAuthentication_401()

    update = {"hashed_password": get_hashed_password(password_change.new_password)}
    user.sqlmodel_update(update)

    await session.commit()
