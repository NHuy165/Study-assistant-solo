from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models_schema.activity.exercise_item import (
    ExerciseItem,
    ExerciseItemUpdate,
)
from backend.src.models_schema.activity.study_activity import (
    StudyActivity,
    StudyActivityInput,
    StudyActivityUpdate,
)
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.user import User

# ----- DUMMY DATA ----- #


# ----- CREATE ----- #


async def create_study_activity(
    session: AsyncSession,
    interaction: Interaction,
    study_activity_input: StudyActivityInput,
) -> StudyActivity:  # type: ignore
    pass


# async def create_study_activity(
#     session: AsyncSession,
#     interaction: Interaction,
#     study_activity_input: StudyActivityInput,
# ) -> tuple[StudyActivity, ReviewActivity | ExerciseActivity]:

#     # === Generates content from model using RAG === #

#     # Gets past conversations
#     past_conversations = await read_llm_responses(
#         session, interaction, settings.N_PAST_CONVERSATIONS
#     )
#     formatted_past_conversations = conversations_formatter(past_conversations)

#     # Retrieval (using the rewritten prompt)
#     rewritten_prompt = await rewrite_prompt(
#         study_activity_input.prompt, formatted_past_conversations
#     )

#     embedded_prompt = await GlobalAPI.embed(rewritten_prompt)
#     document_chunks = await retrieval(
#         session=session,
#         interaction=interaction,
#         raw_prompt=rewritten_prompt,
#         embedded_prompt=embedded_prompt,
#     )
#     formatted_chunks = chunks_formatter(document_chunks)

#     # Augmentation
#     json_schema, response_validator = schema_map[study_activity_input.activity_format]

#     params = StudyActivityParams(
#         prompt=study_activity_input.prompt,
#         context_conversations=formatted_past_conversations,
#         context_document=formatted_chunks,
#         json_schema=json_schema,
#         subject_type=study_activity_input.subject_type,
#         activity_format=study_activity_input.activity_format,
#     )

#     final_prompt = study_activity_augmentation(params)

#     # Generation
#     generated_activity = await GlobalAPI.generate_content(final_prompt)

#     # Validates content from model
#     validated_activity = response_validator.model_validate_json(generated_activity)

#     # === Saves response === #

#     # General activity information
#     study_activity = StudyActivity(
#         prompt=study_activity_input.prompt,
#         activity_type=study_activity_input.activity_type,
#         activity_format=study_activity_input.activity_format,
#         subject_type=study_activity_input.subject_type,
#         name=validated_activity.name,
#         description=validated_activity.description,
#         interaction=interaction,
#     )

#     session.add(study_activity)

#     await session.commit()
#     await session.refresh(study_activity)

#     return study_activity

# ----- READ ----- #


async def read_all_study_activity(
    session: AsyncSession,
    interaction: Interaction,
) -> list[StudyActivity]:  # type: ignore
    pass


async def read_study_activity_complete(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
) -> StudyActivity:  # type: ignore
    pass


# ----- UPDATE ----- #


async def update_study_activity(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
    study_activity_update: StudyActivityUpdate,
) -> StudyActivity:  # type: ignore
    pass


async def answer_exercise_item(
    user: User,
    session: AsyncSession,
    exercise_item_id: int,
    exercise_item_update: ExerciseItemUpdate,
) -> ExerciseItem:  # type: ignore
    pass


async def submit_exercise_activity(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
) -> StudyActivity:  # type: ignore
    pass


# ----- DELETE ----- #


async def delete_study_activity(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
) -> None:
    pass
