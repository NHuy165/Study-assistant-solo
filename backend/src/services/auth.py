from datetime import datetime

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from backend.src.core.dependencies import check_in
from backend.src.core.security import create_token, verify_password
from backend.src.exceptions.core import ExceptionAuthentication_401
from backend.src.models_schema.auth.auth import Token
from backend.src.models_schema.user.check_in import CheckIn
from backend.src.models_schema.user.user import User

DUMMY_PASSWORD_HASH = "$argon2id$v=19$m=65536,t=3,p=4$G2cBxzF8vfN1DcBl8MKqhA$MeuvTNFv+5KpsyY6cxegwP1P2UbrWLq6Xyaq/S+h8v0"


async def authenticate_user(
    session: AsyncSession, email: EmailStr, password: str
) -> tuple[User, CheckIn | None]:
    query = (
        select(User, CheckIn)
        .select_from(User)
        .outerjoin(CheckIn)
        .where(User.email == email)
        .order_by(col(CheckIn.time).desc())
        .limit(1)
    )
    row = (await session.execute(query)).first()

    if row is None:
        # Mimics password check delay
        verify_password("WRONG PASSWORD", DUMMY_PASSWORD_HASH)
        raise ExceptionAuthentication_401()

    user, last_check_in = row

    assert isinstance(user, User)
    assert isinstance(last_check_in, CheckIn | None)

    if not verify_password(password, user.hashed_password):
        raise ExceptionAuthentication_401()

    return user, last_check_in


async def login_for_token(
    session: AsyncSession,
    current_datetime: datetime,
    email: EmailStr,
    password: str,
) -> Token:
    user, last_check_in = await authenticate_user(session, email, password)

    await check_in(
        user=user,
        session=session,
        current_datetime=current_datetime,
        last_check_in=last_check_in,
    )

    await session.close()

    data = {"sub": str(user.id)}

    token_str = create_token(data, current_datetime)

    return Token(access_token=token_str, token_type="bearer")
