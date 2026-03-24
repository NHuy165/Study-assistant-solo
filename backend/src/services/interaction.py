from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.src.exceptions.core import ExceptionNotFound_404
from backend.src.models_schema.interaction import (
    Interaction,
    InteractionInput,
    InteractionUpdate,
)
from backend.src.models_schema.user import User

# ----- CREATE ----- #


async def create_interaction(
    user: User, session: AsyncSession, interaction_input: InteractionInput
) -> Interaction:
    interaction = Interaction(
        **interaction_input.model_dump(),
        user=user,
    )

    session.add(interaction)
    await session.commit()
    await session.refresh(interaction)

    return interaction


# ----- READ ----- #


async def read_all_interactions(user: User, session: AsyncSession) -> list[Interaction]:
    query = select(Interaction).where(Interaction.user_id == user.id)
    interactions = (await session.execute(query)).scalars().all()

    return list(interactions)


# ----- UPDATE ----- #


async def update_interaction(
    user: User,
    session: AsyncSession,
    interaction_id: int,
    interaction_update: InteractionUpdate,
) -> Interaction:
    query = select(Interaction).where(
        Interaction.user_id == user.id, Interaction.id == interaction_id
    )
    interaction = (await session.execute(query)).scalars().first()

    if interaction is None:
        raise ExceptionNotFound_404(
            "Interaction", {"user_id": user.id, "id": interaction_id}
        )

    # Update logic
    update_data = interaction_update.model_dump(exclude_unset=True)
    interaction.sqlmodel_update(update_data)

    await session.commit()
    await session.refresh(interaction)

    return interaction


# ----- DELETE ----- #


async def delete_interaction(
    user: User, session: AsyncSession, interaction_id: int
) -> None:
    query = select(Interaction).where(
        Interaction.user_id == user.id, Interaction.id == interaction_id
    )
    result = (await session.execute(query)).scalars().first()

    if result is None:
        raise ExceptionNotFound_404(
            "Interaction", {"user_id": user.id, "id": interaction_id}
        )

    await session.delete(result)
    await session.commit()
