from types import CoroutineType
from typing import Any, Callable

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models_schema.interaction import Interaction, InteractionInput


@pytest.fixture(name="create_interaction_custom")
async def create_interaction_custom_fixture(
    session: AsyncSession,
    client: AsyncClient,
    login_user_test: None,
) -> Callable[[str], CoroutineType[Any, Any, int]]:
    async def create_interaction_custom(interaction_name: str) -> int:
        interaction_input = InteractionInput(
            name=interaction_name, description=f"{interaction_name}-description"
        )  # type: ignore

        response = await client.post(
            "/api/interaction/create",
            json=interaction_input.model_dump(),
        )

        interaction_id = response.json().get("id")

        session.expire_all()

        return interaction_id  # type: ignore

    return create_interaction_custom


@pytest.fixture(name="create_interaction_test")
async def create_interaction_test_fixture(
    create_interaction_custom: Callable[[str], CoroutineType[Any, Any, int]],
) -> int:
    interaction_id = await create_interaction_custom("test")
    return interaction_id
