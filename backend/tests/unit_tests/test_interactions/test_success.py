from types import CoroutineType
from typing import Any, Callable

from httpx import AsyncClient

from backend.src.models_schema.interaction import (
    InteractionInput,
    InteractionOutput,
    InteractionUpdate,
)
from backend.tests.utils.validators import (
    validate_contents,
    validate_model,
    validate_status_code,
)


async def test_create_interaction(client: AsyncClient, login_user_test: None) -> None:
    """
    Creates an interaction.
    """
    interaction_input = InteractionInput(name="test", description="test-description")

    response = await client.post(
        "/api/interaction/create",
        json=interaction_input.model_dump(),
    )

    validate_status_code(response, 200)
    validate_model(response, InteractionOutput)
    validate_contents(response, interaction_input.model_dump())


async def test_read_all_interactions(
    client: AsyncClient,
    create_interaction_custom: Callable[[str], CoroutineType[Any, Any, int]],
) -> None:
    """
    Reads all interactions.
    """
    await create_interaction_custom("interaction1")
    await create_interaction_custom("interaction2")

    response = await client.get("/api/interaction/")

    validate_status_code(response, 200)
    validate_model(response, list[InteractionOutput])
    validate_contents(
        response,
        [
            {"name": "interaction1"},
            {"name": "interaction2"},
        ],
    )


async def test_update_interaction(
    client: AsyncClient,
    create_interaction_test: int,
) -> None:
    """
    Updates an interaction.
    """
    interaction_update = InteractionUpdate(
        name="updated", description="updated-description"
    )

    response = await client.patch(
        f"/api/interaction/{create_interaction_test}",
        json=interaction_update.model_dump(),
    )

    validate_status_code(response, 200)
    validate_model(response, InteractionOutput)
    validate_contents(response, interaction_update.model_dump())


async def test_delete_interaction(
    client: AsyncClient,
    create_interaction_test: int,
) -> None:
    """
    Deletes an interaction;
    """
    response_delete = await client.delete(
        f"/api/interaction/{create_interaction_test}",
    )

    validate_status_code(response_delete, 204)

    response_delete_2 = await client.delete(
        f"/api/interaction/{create_interaction_test}",
    )

    validate_status_code(response_delete_2, 404)
