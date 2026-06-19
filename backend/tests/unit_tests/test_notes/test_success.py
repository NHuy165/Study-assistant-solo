from types import CoroutineType
from typing import Any, Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models_schema.interaction.interaction import (
    Interaction,
    InteractionInput,
    InteractionOutput,
    InteractionUpdate,
)
from backend.src.models_schema.note.note import Note, NoteInput, NoteOutput, NoteUpdate
from backend.src.models_schema.user.user import User
from backend.tests.utils.validators import (
    validate_object_contents,
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)


async def test_create_note(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
) -> None:
    """
    Creates a note.
    """
    note_input = NoteInput(
        name="test",
        description="test-description",
        content="test-content",
    )

    response = await client.post(
        f"/api/note/{create_interaction_test.id}/upload",
        json=note_input.model_dump(),
    )

    validate_status_code(response, 200)
    validate_response_model(response, NoteOutput)
    validate_response_contents(response, note_input.model_dump())


async def test_read_all_notes(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_note_custom: Callable[[Interaction, str], CoroutineType[Any, Any, Note]],
) -> None:
    """
    Reads all interactions.
    """
    await create_note_custom(create_interaction_test, "test1")
    await create_note_custom(create_interaction_test, "test2")

    response = await client.get(
        f"/api/note/{create_interaction_test.id}/",
    )

    validate_status_code(response, 200)
    validate_response_model(response, list[NoteOutput])
    validate_response_contents(
        response,
        [
            {"name": "test1-note"},
            {"name": "test2-note"},
        ],
    )


async def test_update_note(
    session: AsyncSession,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_note_custom: Callable[[Interaction, str], CoroutineType[Any, Any, Note]],
) -> None:
    """
    Updates a note.
    """
    note = await create_note_custom(create_interaction_test, "test")

    note_update = NoteUpdate(
        name="updated",
        description="updated-description",
        content="updated-content",
    )

    response = await client.patch(
        f"/api/note/{note.id}",
        json=note_update.model_dump(exclude_unset=True),
    )

    validate_status_code(response, 200)
    validate_response_model(response, NoteOutput)
    validate_response_contents(
        response,
        note_update.model_dump(exclude_unset=True),
    )

    # Validates database data
    await session.refresh(note)

    validate_object_contents(note, note_update.model_dump(exclude_unset=True))


async def test_delete_note(
    session: AsyncSession,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_note_custom: Callable[[Interaction, str], CoroutineType[Any, Any, Note]],
) -> None:
    """
    Deletes a note.
    """
    note = await create_note_custom(create_interaction_test, "test")

    response1 = await client.delete(
        f"/api/note/{note.id}",
    )

    validate_status_code(response1, 204)

    response2 = await client.delete(
        f"/api/note/{note.id}",
    )

    validate_status_code(response2, 404)
