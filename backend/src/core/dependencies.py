from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.src.core.config import settings
from backend.src.core.database import get_async_session
from backend.src.exceptions.core import (
    ExceptionAuthentication_401,
    ExceptionNotFound_404,
)
from backend.src.models_schema.auth import TokenData
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
):
    # No token failure
    if token is None:
        raise ExceptionAuthentication_401()

    try:
        contents = jwt.decode(
            jwt=token,
            key=settings.PRIVATE_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        validated_contents = TokenData.model_validate(contents)

    # Invalid token failure
    except jwt.InvalidTokenError:
        raise ExceptionAuthentication_401()

    # Token with wrong format failure
    except ValidationError:
        raise ExceptionAuthentication_401()

    user = await session.get(User, validated_contents.sub)

    # User not found failure
    if user is None:
        raise ExceptionAuthentication_401()

    now = datetime.now(timezone.utc)

    if user.last_logged_in_at is None:
        user.login_streak = 1
        user.longest_login_streak = 1
    else:
        if now.date() - user.last_logged_in_at.date() == timedelta(days=1):
            user.login_streak += 1
            if user.login_streak > user.longest_login_streak:
                user.longest_login_streak = user.login_streak

        elif now.date() - user.last_logged_in_at.date() > timedelta(days=1):
            user.login_streak = 1

    user.last_logged_in_at = now

    return user


UserDep = Annotated[User, Depends(get_current_user)]


async def get_interaction_id(
    user: UserDep, session: SessionDep, interaction_id: Annotated[int, Path()]
) -> Interaction:
    query = select(Interaction).where(
        Interaction.user_id == user.id,
        Interaction.id == interaction_id,
        Interaction.is_deleted == False,
    )

    interaction = (await session.execute(query)).scalars().first()

    await session.commit()

    if interaction is None:
        raise ExceptionNotFound_404(
            "Interaction",
            {"user_id": user.id, "id": interaction_id, "is_deleted": False},
        )

    return interaction


InteractionDep = Annotated[Interaction, Depends(get_interaction_id)]
