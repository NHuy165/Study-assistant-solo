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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

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

    return user


UserDep = Annotated[User, Depends(get_current_user)]


async def get_interaction_id(
    user: UserDep, session: SessionDep, interaction_id: Annotated[int, Path()]
) -> Interaction:
    query = select(Interaction).where(
        Interaction.user_id == user.id, Interaction.id == interaction_id
    )

    interaction = (await session.execute(query)).scalars().first()

    if interaction is None:
        raise ExceptionNotFound_404(
            "Interaction", {"user_id": user.id, "id": interaction_id}
        )

    return interaction


InteractionDep = Annotated[Interaction, Depends(get_interaction_id)]
