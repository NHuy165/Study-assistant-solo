from types import CoroutineType
from typing import Any, Callable

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.src.models_schema.interaction.interaction import (
    Interaction,
    InteractionInput,
)
from backend.src.models_schema.user.user import User


@pytest.fixture(name="create_interaction_custom")
async def create_interaction_custom_fixture(
    session: AsyncSession,
) -> Callable[[User, str], CoroutineType[Any, Any, int]]:
    """
    Returns a function that creates an interaction with a custom name attached to a custom user.
    """

    async def create_interaction_custom(user: User, interaction_name: str) -> int:
        interaction = Interaction(
            name=interaction_name,
            description=f"{interaction_name}-description",
            user=user,
        )  # type: ignore

        session.add(interaction)
        await session.commit()
        assert interaction.id is not None

        return interaction.id

    return create_interaction_custom


@pytest.fixture(name="create_interaction_test")
async def create_interaction_test_fixture(
    session: AsyncSession,
    create_interaction_custom: Callable[[User, str], CoroutineType[Any, Any, int]],
) -> int:
    """
    Automatically creates an interaction with the name "test", attached to the user "test".
    """
    user = (
        (await session.execute(select(User).where(User.email == "test@gmail.com")))
        .scalars()
        .first()
    )
    assert user is not None

    interaction_id = await create_interaction_custom(user, "test")
    return interaction_id
