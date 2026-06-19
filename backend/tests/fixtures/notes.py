from datetime import datetime, timezone
from types import CoroutineType
from typing import Any, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.src.models_schema.interaction.interaction import (
    Interaction,
)
from backend.src.models_schema.note.note import Note
from backend.src.models_schema.user.user import User


@pytest.fixture(name="create_note_custom")
async def create_note_custom_fixture(
    session: AsyncSession,
) -> Callable[[Interaction, str], CoroutineType[Any, Any, Note]]:
    """
    Returns a function that creates a note attached to an interaction.
    """

    async def create_note_custom(interaction: Interaction, note_name: str) -> Note:
        note = Note(
            name=f"{note_name}-note",
            description=f"{note_name}-description",
            content=f"{note_name}-content",
            created_at=datetime.now(timezone.utc),
            interaction=interaction,
        )

        session.add(note)
        await session.commit()

        return note

    return create_note_custom
