from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from backend.src.core.config import settings
from backend.src.core.database import get_async_session
from backend.src.exceptions.core import (
    ExceptionAuthentication_401,
    ExceptionNotFound_404,
)
from backend.src.models_schema.auth.auth import TokenData
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.user.check_in import CheckIn
from backend.src.models_schema.user.user import User

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

    # Fetches user
    query = select(User).where(User.id == validated_contents.sub)
    user = (await session.execute(query)).scalars().first()

    if user is None:
        raise ExceptionAuthentication_401()

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
