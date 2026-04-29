from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from backend.src.core.ai_api import ExceptionRequest_400, GlobalAPI
from backend.src.core.config import settings
from backend.src.exceptions.core import ExceptionNotFound_404
from backend.src.models_schema.activity.exercise_item import (
    ExerciseItem,
    ExerciseItemUpdate,
)
from backend.src.models_schema.activity.exercise_item_content import ExerciseItemContent
from backend.src.models_schema.activity.json_validation import (
    FlashcardsJsonSchema,
    GapFillJsonSchema,
    MCQJsonSchema,
    OpenEndedJsonSchema,
    StudyActivityValidationBase,
)
from backend.src.models_schema.activity.review_item import ReviewItem
from backend.src.models_schema.activity.review_item_content import ReviewItemContent
from backend.src.models_schema.activity.study_activity import (
    StudyActivity,
    StudyActivityInput,
    StudyActivityOutputComplete,
    StudyActivityUpdate,
)
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    ExerciseItemContentType,
    ReviewItemContentType,
    StudyActivityFormat,
    StudyActivityType,
)
from backend.src.models_schema.RAG.augmentation import StudyActivityParams
from backend.src.models_schema.user import User
from backend.src.RAG.augmentation.core.specific_augmentations import (
    study_activity_augmentation,
)
from backend.src.RAG.augmentation.formatters.chunks.core import chunks_formatter
from backend.src.RAG.augmentation.formatters.conversations.core import (
    conversations_formatter,
)
from backend.src.RAG.augmentation.prompts_formatting.instruction_schemas import (
    flashcards_schema,
    gap_fill_schema,
    multiple_choice_questions_schema,
    open_ended_schema,
)
from backend.src.RAG.retrieval.core import retrieval
from backend.src.RAG.retrieval.prompt_rewrite import rewrite_prompt
from backend.src.services.llm_response import read_llm_responses

# ----- CREATE ----- #

schema_map: dict[
    StudyActivityFormat | StudyActivityFormat,
    tuple[str, type[StudyActivityValidationBase]],
] = {
    StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS: (
        multiple_choice_questions_schema,
        MCQJsonSchema,
    ),
    StudyActivityFormat.FLASHCARDS: (flashcards_schema, FlashcardsJsonSchema),
    StudyActivityFormat.GAP_FILL: (gap_fill_schema, GapFillJsonSchema),
    StudyActivityFormat.OPEN_ENDED: (open_ended_schema, OpenEndedJsonSchema),
}


async def save_multiple_choice_questions(
    session: AsyncSession,
    activity_data: StudyActivityValidationBase,
    study_activity: StudyActivity,
) -> None:
    assert isinstance(activity_data, MCQJsonSchema)

    n_items = len(activity_data.activity_items)
    if n_items == 0:
        return

    assert study_activity.total_score is not None
    question_score = study_activity.total_score / n_items

    for i_item in range(n_items):
        # Saving the item
        exercise_item = ExerciseItem(
            max_score=question_score,
            question=activity_data.activity_items[i_item].question,
            study_activity=study_activity,
        )
        session.add(exercise_item)
        await session.commit()
        await session.refresh(exercise_item)

        # Saving the contents of the item
        n_contents = len(activity_data.activity_items[i_item].answers)
        for i_content in range(n_contents):
            exercise_item_content = ExerciseItemContent(
                content=activity_data.activity_items[i_item].answers[i_content],
                type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
                is_correct=True
                if i_content == activity_data.activity_items[i_item].correct
                else False,
                exercise_item=exercise_item,
            )
            session.add(exercise_item_content)

        await session.commit()


async def save_open_ended(
    session: AsyncSession,
    activity_data: StudyActivityValidationBase,
    study_activity: StudyActivity,
) -> None:
    assert isinstance(activity_data, OpenEndedJsonSchema)

    n_items = len(activity_data.activity_items)
    if n_items == 0:
        return

    assert study_activity.total_score is not None
    question_score = study_activity.total_score / n_items

    for i_item in range(n_items):
        # Saving the item
        exercise_item = ExerciseItem(
            max_score=question_score,
            question=activity_data.activity_items[i_item].question,
            study_activity=study_activity,
        )
        session.add(exercise_item)

    await session.commit()


async def save_gap_fill(
    session: AsyncSession,
    activity_data: StudyActivityValidationBase,
    study_activity: StudyActivity,
) -> None:
    assert isinstance(activity_data, GapFillJsonSchema)

    n_items = len(activity_data.activity_items)
    if n_items == 0:
        return

    for i_item in range(n_items):
        # Saving the item
        review_item = ReviewItem(
            study_activity=study_activity,
        )
        session.add(review_item)
        await session.commit()
        await session.refresh(review_item)

        # Saving the contents of the item
        text_content = ReviewItemContent(
            content=activity_data.activity_items[i_item].text,
            type=ReviewItemContentType.GAP_FILL_TEXT,
            review_item=review_item,
        )
        session.add(text_content)

        n_correct_contents = len(activity_data.activity_items[i_item].correct)
        for i_correct_content in range(n_correct_contents):
            review_item_content = ReviewItemContent(
                content=activity_data.activity_items[i_item].correct[i_correct_content],
                type=ReviewItemContentType.GAP_FILL_CORRECT,
                review_item=review_item,
            )
            session.add(review_item_content)

        n_distractors_contents = len(activity_data.activity_items[i_item].distractors)
        for i_distractor_content in range(n_distractors_contents):
            review_item_content = ReviewItemContent(
                content=activity_data.activity_items[i_item].distractors[
                    i_distractor_content
                ],
                type=ReviewItemContentType.GAP_FILL_DISTRACTOR,
                review_item=review_item,
            )
            session.add(review_item_content)

        await session.commit()


async def save_flashcards(
    session: AsyncSession,
    activity_data: StudyActivityValidationBase,
    study_activity: StudyActivity,
) -> None:
    assert isinstance(activity_data, FlashcardsJsonSchema)

    n_items = len(activity_data.activity_items)
    if n_items == 0:
        return

    for i_item in range(n_items):
        # Saving the item
        review_item = ReviewItem(
            study_activity=study_activity,
        )
        session.add(review_item)
        await session.commit()
        await session.refresh(review_item)

        # Saving the contents of the item
        front_content = ReviewItemContent(
            content=activity_data.activity_items[i_item].front,
            type=ReviewItemContentType.FLASHCARDS_FRONT,
            review_item=review_item,
        )
        session.add(front_content)

        back_content = ReviewItemContent(
            content=activity_data.activity_items[i_item].back,
            type=ReviewItemContentType.FLASHCARDS_BACK,
            review_item=review_item,
        )
        session.add(back_content)

        await session.commit()


save_mapper = {
    StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS: save_multiple_choice_questions,
    StudyActivityFormat.OPEN_ENDED: save_open_ended,
    StudyActivityFormat.FLASHCARDS: save_flashcards,
    StudyActivityFormat.GAP_FILL: save_gap_fill,
}


async def create_study_activity(
    session: AsyncSession,
    interaction: Interaction,
    study_activity_input: StudyActivityInput,
) -> StudyActivityOutputComplete:

    # === Generates content from model using RAG === #

    # Gets past conversations
    past_conversations = await read_llm_responses(
        session, interaction, settings.N_PAST_CONVERSATIONS
    )
    formatted_past_conversations = conversations_formatter(past_conversations)

    # Rewrites prompt
    rewritten_prompt = await rewrite_prompt(
        study_activity_input.prompt, formatted_past_conversations
    )

    # Retrieval (using the rewritten prompt)
    embedded_prompt = await GlobalAPI.embed(rewritten_prompt)
    document_chunks = await retrieval(
        session=session,
        interaction=interaction,
        raw_prompt=rewritten_prompt,
        embedded_prompt=embedded_prompt,
    )
    formatted_chunks = chunks_formatter(document_chunks)

    # Augmentation
    json_schema, response_validator = schema_map[study_activity_input.activity_format]

    params = StudyActivityParams(
        prompt=study_activity_input.prompt,
        context_conversations=formatted_past_conversations,
        context_document=formatted_chunks,
        json_schema=json_schema,
        subject_type=study_activity_input.subject_type,
        activity_format=study_activity_input.activity_format,
    )

    final_prompt = study_activity_augmentation(params)

    # Generation
    generated_activity = await GlobalAPI.generate_content(final_prompt)

    # Validates content from model
    validated_activity = response_validator.model_validate_json(generated_activity)

    # === Saves response === #

    study_activity = StudyActivity(
        prompt=study_activity_input.prompt,
        activity_type=study_activity_input.activity_type,
        activity_format=study_activity_input.activity_format,
        subject_type=study_activity_input.subject_type,
        name=validated_activity.name,
        description=validated_activity.description,
        total_score=settings.DEFAULT_EXERCISE_TOTAL_SCORE
        if study_activity_input.activity_type == StudyActivityType.EXERCISE
        else None,
        interaction=interaction,
    )

    session.add(study_activity)
    await session.commit()
    await session.refresh(study_activity)

    saver = save_mapper[study_activity_input.activity_format]
    await saver(
        session=session, activity_data=validated_activity, study_activity=study_activity
    )

    # === Refetch with all contents === #

    await session.refresh(study_activity)

    query = select(StudyActivity).where(StudyActivity.id == study_activity.id)

    if study_activity_input.activity_type == StudyActivityType.EXERCISE:
        query = query.options(
            selectinload(StudyActivity.exercise_items).selectinload(  # type: ignore
                ExerciseItem.contents  # type: ignore
            )
        )

    else:
        query = query.options(
            selectinload(StudyActivity.review_items).selectinload(ReviewItem.contents)  # type: ignore
        )

    study_activity = (await session.execute(query)).scalars().first()

    study_activity_output_complete = StudyActivityOutputComplete.model_validate(
        study_activity
    )

    return study_activity_output_complete


# ----- READ ----- #


async def read_all_study_activity(
    session: AsyncSession,
    interaction: Interaction,
) -> list[StudyActivity]:
    query = select(StudyActivity).where(StudyActivity.interaction_id == interaction.id)
    study_activities = (await session.execute(query)).scalars().all()

    return list(study_activities)


async def read_study_activity_complete(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
) -> StudyActivityOutputComplete:

    query = (
        select(StudyActivity)
        .join(Interaction)
        .where(StudyActivity.id == study_activity_id, Interaction.user_id == user.id)
        .options(
            selectinload(StudyActivity.review_items).selectinload(ReviewItem.contents),  # type: ignore
            selectinload(StudyActivity.exercise_items).selectinload(  # type: ignore
                ExerciseItem.contents  # type: ignore
            ),
        )
    )
    study_activity = (await session.execute(query)).scalars().first()

    if study_activity is None:
        raise ExceptionNotFound_404(
            "StudyActivity",
            {
                "id": study_activity_id,
                "interaction.user_id": user.id,
            },
        )

    if study_activity.is_submitted:
        study_activity_output_complete = StudyActivityOutputComplete.model_validate(
            study_activity, context={"show_answers": True}
        )
    else:
        study_activity_output_complete = StudyActivityOutputComplete.model_validate(
            study_activity
        )

    return study_activity_output_complete


# ----- UPDATE ----- #


async def update_study_activity(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
    study_activity_update: StudyActivityUpdate,
) -> StudyActivity:  # type: ignore
    query = (
        select(StudyActivity)
        .join(Interaction)
        .where(StudyActivity.id == study_activity_id, Interaction.user_id == user.id)
    )

    study_activity = (await session.execute(query)).scalars().first()

    if study_activity is None:
        raise ExceptionNotFound_404(
            "StudyActivity",
            {
                "id": study_activity_id,
                "interaction.user_id": user.id,
            },
        )

    update_data = study_activity_update.model_dump(exclude_unset=True)

    study_activity.sqlmodel_update(update_data)

    session.add(study_activity)
    await session.commit()
    await session.refresh(study_activity)

    return study_activity


async def answer_exercise_item(
    user: User,
    session: AsyncSession,
    exercise_item_id: int,
    exercise_item_update: ExerciseItemUpdate,
) -> ExerciseItem:  # type: ignore
    query = (
        select(ExerciseItem, StudyActivity)
        .join(StudyActivity)
        .join(Interaction)
        .where(ExerciseItem.id == exercise_item_id, Interaction.user_id == user.id)
        .options(selectinload(ExerciseItem.contents))  # type: ignore
    )

    row = (await session.execute(query)).first()

    if row is None:
        raise ExceptionNotFound_404(
            "ExerciseItem",
            {
                "id": exercise_item_id,
                "interaction.user_id": user.id,
            },
        )

    exercise_item, study_activity = row

    assert isinstance(exercise_item, ExerciseItem)
    assert isinstance(study_activity, StudyActivity)

    if study_activity.activity_format == StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS:
        if not isinstance(exercise_item_update.attempt, int):
            raise ExceptionRequest_400(
                custom_message="Answers to multiple choice questions need to be an integer pointing to the id of the correct answer."
            )

        if exercise_item_update.attempt not in (
            content.id for content in exercise_item.contents
        ):
            raise ExceptionRequest_400(
                custom_message="Answer did not match the id of any of the answers of the current question."
            )
    else:
        if not isinstance(exercise_item_update.attempt, str):
            raise ExceptionRequest_400(
                custom_message="Answer needs to be of type string."
            )

    exercise_item.attempt = str(exercise_item_update.attempt)

    session.add(exercise_item)
    await session.commit()
    await session.refresh(exercise_item)

    return exercise_item


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
    query = (
        select(StudyActivity)
        .join(Interaction)
        .where(StudyActivity.id == study_activity_id, Interaction.user_id == user.id)
    )

    study_activity = (await session.execute(query)).scalars().first()

    if study_activity is None:
        raise ExceptionNotFound_404(
            "StudyActivity",
            {
                "id": study_activity_id,
                "interaction.user_id": user.id,
            },
        )

    await session.delete(study_activity)
    await session.commit()
