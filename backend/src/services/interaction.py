from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import and_, col, delete, select

from backend.src.exceptions.core import ExceptionNotFound_404
from backend.src.models_schema.activity.exercise_item import ExerciseItem
from backend.src.models_schema.activity.review_item import ReviewItem
from backend.src.models_schema.activity.study_activity import StudyActivity
from backend.src.models_schema.document import Document
from backend.src.models_schema.interaction import (
    Interaction,
    InteractionInput,
    InteractionUpdate,
)
from backend.src.models_schema.llm_response import LLMResponse
from backend.src.models_schema.note import Note
from backend.src.models_schema.user import User
from backend.src.services.study_activity import ExerciseItemContent, ReviewItemContent

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
    query = select(Interaction).where(
        Interaction.user_id == user.id, Interaction.is_deleted == False
    )
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
        Interaction.user_id == user.id,
        Interaction.id == interaction_id,
        Interaction.is_deleted == False,
    )
    interaction = (await session.execute(query)).scalars().first()

    if interaction is None:
        raise ExceptionNotFound_404(
            "Interaction",
            {
                "user_id": user.id,
                "id": interaction_id,
                "is_deleted": False,
            },
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
    query = (
        select(Interaction)
        .where(Interaction.user_id == user.id, Interaction.id == interaction_id)
        .options(
            selectinload(
                Interaction.study_activities.and_(StudyActivity.is_deleted == False)  # type: ignore
            ).selectinload(
                StudyActivity.review_items.and_(ReviewItem.is_deleted == False)  # type: ignore
            ),
            selectinload(
                Interaction.study_activities.and_(StudyActivity.is_deleted == False)  # type: ignore
            ).selectinload(
                StudyActivity.exercise_items.and_(ExerciseItem.is_deleted == False)  # type: ignore
            ),
        )
    )
    interaction = (await session.execute(query)).scalars().first()

    if interaction is None:
        raise ExceptionNotFound_404(
            "Interaction", {"user_id": user.id, "id": interaction_id}
        )

    # Soft deletes study activities
    for activity in interaction.study_activities:
        activity.is_deleted = True
        for item in activity.items:
            item.is_deleted = True

    # Hard deletes the item contents
    subquery_review = (
        select(ReviewItem.id)
        .join(StudyActivity)
        .where(StudyActivity.interaction_id == interaction_id)
    )
    query_delete_review_contents = delete(ReviewItemContent).where(
        col(ReviewItemContent.review_item_id).in_(subquery_review)
    )

    subquery_exercise = (
        select(ExerciseItem.id)
        .join(StudyActivity)
        .where(StudyActivity.interaction_id == interaction_id)
    )
    query_delete_exercise_contents = delete(ExerciseItemContent).where(
        col(ExerciseItemContent.exercise_item_id).in_(subquery_exercise)
    )

    await session.execute(query_delete_review_contents)
    await session.execute(query_delete_exercise_contents)

    # Hard deletes the other things
    query_delete_document = delete(Document).where(
        col(Document.interaction_id == interaction_id)
    )
    query_delete_llmresponse = delete(LLMResponse).where(
        col(LLMResponse.interaction_id == interaction_id)
    )
    query_delete_note = delete(Note).where(col(Note.interaction_id == interaction_id))

    await session.execute(query_delete_document)
    await session.execute(query_delete_llmresponse)
    await session.execute(query_delete_note)

    interaction.is_deleted = True

    await session.commit()
