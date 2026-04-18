from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.ai_api import GlobalAPI
from backend.src.core.config import settings
from backend.src.exceptions.core import ExceptionRequest_400
from backend.src.models_schema.activity.exercise_activity import (
    ExerciseActivity,
    ExerciseActivityInput,
)
from backend.src.models_schema.activity.json_validation import (
    ExerciseActivityValidationBase,
    ReviewActivityValidationBase,
)
from backend.src.models_schema.activity.review_activity import (
    ReviewActivity,
    ReviewActivityInput,
)
from backend.src.models_schema.activity.study_activity import (
    StudyActivity,
    StudyActivityInput,
)
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import StudyActivityType
from backend.src.models_schema.RAG.augmentation import (
    StudyActivityParams,
)
from backend.src.RAG.augmentation.chunk_rewriting.rewrite import rewrite_prompt
from backend.src.RAG.augmentation.core.specific_augmentations import (
    study_activity_augmentation,
)
from backend.src.RAG.augmentation.formatters.chunks.core import chunks_formatter
from backend.src.RAG.augmentation.formatters.conversations.core import (
    conversations_formatter,
)
from backend.src.RAG.augmentation.study_activity.type_mappings import schema_map
from backend.src.RAG.retrieval.core import retrieval
from backend.src.services.llm_response import read_llm_responses

# ----- CREATE ----- #


async def create_study_activity(
    session: AsyncSession,
    interaction: Interaction,
    study_activity_input: StudyActivityInput,
    review_activity_input: ReviewActivityInput | None = None,
    exercise_activity_input: ExerciseActivityInput | None = None,
) -> tuple[StudyActivity, ReviewActivity | ExerciseActivity]:

    is_review = study_activity_input.study_activity_type == StudyActivityType.REVIEW
    is_exercise = study_activity_input.study_activity_type == StudyActivityType.EXERCISE

    # === Validate input === #

    if is_review and review_activity_input is None:
        raise ExceptionRequest_400(
            "Selected REVIEW type for study activity but no review_activity_input provided."
        )
    if is_exercise and exercise_activity_input is None:
        raise ExceptionRequest_400(
            "Selected REVIEW type for study activity but no exercise_activity_input provided."
        )

    # === Generates content from model using RAG === #

    # Gets past conversations
    past_conversations = await read_llm_responses(
        session, interaction, settings.N_PAST_CONVERSATIONS
    )
    formatted_past_conversations = conversations_formatter(past_conversations)

    # Retrieval (using the rewritten prompt)
    rewritten_prompt = await rewrite_prompt(
        study_activity_input.prompt, formatted_past_conversations
    )

    embedded_prompt = await GlobalAPI.embed(rewritten_prompt)
    document_chunks = await retrieval(
        session=session,
        interaction=interaction,
        raw_prompt=rewritten_prompt,
        embedded_prompt=embedded_prompt,
    )
    formatted_chunks = chunks_formatter(document_chunks)

    # Augmentation
    if is_exercise:
        assert exercise_activity_input is not None
        json_schema, response_validator = schema_map[
            exercise_activity_input.exercise_activity_type
        ]
        study_activity_type = exercise_activity_input.exercise_activity_type

    else:
        assert review_activity_input is not None
        json_schema, response_validator = schema_map[
            review_activity_input.review_activity_type
        ]
        study_activity_type = review_activity_input.review_activity_type

    params = StudyActivityParams(
        prompt=study_activity_input.prompt,
        context_conversations=formatted_past_conversations,
        context_document=formatted_chunks,
        json_schema=json_schema,
        subject_type=study_activity_input.subject_type,
        study_activity_type=study_activity_type,
    )

    final_prompt = study_activity_augmentation(params)

    # Generation
    generated_activity = await GlobalAPI.generate_content(final_prompt)

    # Validates content from model
    validated_activity = response_validator.model_validate_json(generated_activity)

    # === Saves response === #

    # General activity information
    study_activity = StudyActivity(
        prompt=study_activity_input.prompt,
        study_activity_type=study_activity_input.study_activity_type,
        subject_type=study_activity_input.subject_type,
        name=validated_activity.name,
        description=validated_activity.description,
        interaction=interaction,
    )

    # Specific activity information
    if is_exercise:
        assert isinstance(validated_activity, ExerciseActivityValidationBase)
        assert exercise_activity_input is not None

        specific_study_activity = ExerciseActivity(
            questions=jsonable_encoder(validated_activity.questions),
            exercise_activity_type=exercise_activity_input.exercise_activity_type,
            size=len(validated_activity.questions),
            study_activity=study_activity,
        )

    else:
        assert isinstance(validated_activity, ReviewActivityValidationBase)
        assert review_activity_input is not None

        specific_study_activity = ReviewActivity(
            contents=jsonable_encoder(validated_activity.contents),
            review_activity_type=review_activity_input.review_activity_type,
            size=len(validated_activity.contents),
            study_activity=study_activity,
        )

    session.add(study_activity)
    session.add(specific_study_activity)

    await session.commit()
    await session.refresh(study_activity)
    await session.refresh(specific_study_activity)

    return (study_activity, specific_study_activity)
