import json
from datetime import datetime, timezone

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import col, delete, select

from backend.src.core.ai_api import ExceptionRequest_400, GlobalAPI
from backend.src.core.config import settings
from backend.src.exceptions.core import (
    ExceptionLLMError_502,
    ExceptionNotFound_404,
    ExceptionSubmittedExercise_409,
)
from backend.src.models_schema.activity.exercise_item import (
    ExerciseItem,
    ExerciseItemUpdate,
)
from backend.src.models_schema.activity.exercise_item_content import ExerciseItemContent
from backend.src.models_schema.activity.json_schema import (
    FlashcardsSchema,
    GapFillSchema,
    MCQSchema,
    OpenEndedCreationSchema,
    OpenEndedGradingResultItemSchema,
    OpenEndedGradingResultSchema,
    StudyActivityValidationBase,
)
from backend.src.models_schema.activity.review_item import (
    FlashcardInput,
    FlashcardUpdate,
    ReviewItem,
)
from backend.src.models_schema.activity.review_item_content import ReviewItemContent
from backend.src.models_schema.activity.study_activity import (
    FlashcardsActivityInput,
    OpenEndedGradingInitiationSchema,
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
from backend.src.models_schema.RAG.augmentation import (
    AnswersGradingParams,
    StudyActivityParams,
)
from backend.src.models_schema.user import User
from backend.src.RAG.augmentation.core.specific_augmentations import (
    answers_grading_augmentation,
    study_activity_augmentation,
)
from backend.src.RAG.augmentation.formatters.chunks.core import chunks_formatter
from backend.src.RAG.augmentation.formatters.conversations.core import (
    conversations_formatter,
)
from backend.src.RAG.augmentation.prompts_formatting.study_activity_format_prompts import (
    MCQ_format_prompt,
    flashcards_format_prompt,
    gap_fill_format_prompt,
    open_ended_format_prompt,
)
from backend.src.RAG.retrieval.core import retrieval
from backend.src.RAG.retrieval.prompt_rewrite import rewrite_prompt
from backend.src.services.llm_response import read_llm_responses

# ----- CREATE ----- #

format_schema_map: dict[
    StudyActivityFormat,
    tuple[str, type[StudyActivityValidationBase]],
] = {
    StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS: (
        MCQ_format_prompt,
        MCQSchema,
    ),
    StudyActivityFormat.FLASHCARDS: (flashcards_format_prompt, FlashcardsSchema),
    StudyActivityFormat.GAP_FILL: (gap_fill_format_prompt, GapFillSchema),
    StudyActivityFormat.OPEN_ENDED: (open_ended_format_prompt, OpenEndedCreationSchema),
}


async def save_multiple_choice_questions(
    session: AsyncSession,
    activity_data: StudyActivityValidationBase,
    study_activity: StudyActivity,
) -> None:
    assert isinstance(activity_data, MCQSchema)

    n_items = len(activity_data.activity_items)
    if n_items == 0:
        return

    question_score = settings.DEFAULT_EXERCISE_TOTAL_SCORE / n_items

    for i_item in range(n_items):
        # Saving the item
        exercise_item = ExerciseItem(
            max_score=question_score,
            question=activity_data.activity_items[i_item].question,
            study_activity=study_activity,
        )
        session.add(exercise_item)

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


async def save_open_ended(
    session: AsyncSession,
    activity_data: StudyActivityValidationBase,
    study_activity: StudyActivity,
) -> None:
    assert isinstance(activity_data, OpenEndedCreationSchema)

    n_items = len(activity_data.activity_items)
    if n_items == 0:
        return

    question_score = settings.DEFAULT_EXERCISE_TOTAL_SCORE / n_items

    for i_item in range(n_items):
        # Saving the item
        exercise_item = ExerciseItem(
            max_score=question_score,
            question=activity_data.activity_items[i_item].question,
            study_activity=study_activity,
        )
        session.add(exercise_item)


async def save_gap_fill(
    session: AsyncSession,
    activity_data: StudyActivityValidationBase,
    study_activity: StudyActivity,
) -> None:
    assert isinstance(activity_data, GapFillSchema)

    n_items = len(activity_data.activity_items)
    if n_items == 0:
        return

    for i_item in range(n_items):
        # Saving the item
        review_item = ReviewItem(
            study_activity=study_activity,
        )
        session.add(review_item)

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


async def save_flashcards(
    session: AsyncSession,
    activity_data: StudyActivityValidationBase,
    study_activity: StudyActivity,
) -> None:
    assert isinstance(activity_data, FlashcardsSchema)

    n_items = len(activity_data.activity_items)
    if n_items == 0:
        return

    for i_item in range(n_items):
        # Saving the item
        review_item = ReviewItem(
            study_activity=study_activity,
        )
        session.add(review_item)

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
) -> StudyActivity:

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

    # Temporary close
    await session.commit()

    # Augmentation
    json_schema, response_validator = format_schema_map[
        study_activity_input.activity_format
    ]

    params = StudyActivityParams(
        prompt=study_activity_input.prompt,
        context_conversations=formatted_past_conversations,
        context_document=formatted_chunks,
        json_schema=json_schema,
        subject_type=study_activity_input.subject_type,
        activity_format=study_activity_input.activity_format,
    )

    final_prompt = study_activity_augmentation(params)

    i_retry = 0
    while True:
        try:
            # Generation
            generated_activity = await GlobalAPI.generate_material(final_prompt)

            # Validates content from model
            validated_activity = response_validator.model_validate_json(
                generated_activity
            )

            if (
                validated_activity.name == "$!SUBJECT!$"
                and validated_activity.description == "$!SUBJECT!$"
            ):
                raise ExceptionRequest_400(
                    "User prompt contents doesn't match specified subject type."
                )
            if (
                validated_activity.name == "$!FORMAT!$"
                and validated_activity.description == "$!FORMAT!$"
            ):
                raise ExceptionRequest_400(
                    "User prompt contents doesn't match specified activity format."
                )

            break
        except (ExceptionLLMError_502, ValidationError) as e:
            i_retry += 1
            if i_retry >= settings.N_GENERATION_RETRIES:
                if isinstance(e, ExceptionLLMError_502):
                    raise
                else:
                    raise ExceptionLLMError_502(
                        f"Incorrect content format. Details: {e}"
                    )
            continue

    # === Saves response === #

    study_activity = StudyActivity(
        prompt=study_activity_input.prompt,
        activity_type=study_activity_input.activity_type,
        activity_format=study_activity_input.activity_format,
        subject_type=study_activity_input.subject_type,
        name=validated_activity.name,
        description=validated_activity.description,
        interaction=interaction,
    )  # type: ignore

    session.add(study_activity)

    saver = save_mapper[study_activity_input.activity_format]
    await saver(
        session=session, activity_data=validated_activity, study_activity=study_activity
    )

    await session.commit()  # Commits EVERYTHING

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

    assert study_activity is not None

    return study_activity


async def create_flashcards_activity(
    session: AsyncSession,
    interaction: Interaction,
    flashcards_activity_input: FlashcardsActivityInput,
) -> StudyActivity:

    flashcards_activity = StudyActivity(
        prompt=None,
        activity_type=StudyActivityType.REVIEW,
        activity_format=StudyActivityFormat.FLASHCARDS,
        subject_type=flashcards_activity_input.subject_type,
        name=flashcards_activity_input.name,
        description=flashcards_activity_input.description,
        interaction=interaction,
    )  # type: ignore

    session.add(flashcards_activity)
    await session.commit()
    await session.refresh(flashcards_activity)

    return flashcards_activity


async def add_flashcards(
    user: User,
    session: AsyncSession,
    flashcard_inputs: list[FlashcardInput],
    flashcards_activity_id: int,
) -> StudyActivityOutputComplete:
    query = (
        select(StudyActivity)
        .join(Interaction)
        .where(
            StudyActivity.id == flashcards_activity_id,
            StudyActivity.activity_format == StudyActivityFormat.FLASHCARDS,
            StudyActivity.is_deleted == False,
            Interaction.user_id == user.id,
        )
    )
    flashcards_activity = (await session.execute(query)).scalars().first()

    if flashcards_activity is None:
        raise ExceptionNotFound_404(
            "StudyActivity",
            {
                "id": flashcards_activity_id,
                "user_id": user.id,
                "activity_format": StudyActivityFormat.FLASHCARDS.value,
                "is_deleted": False,
            },
        )

    for inp in flashcard_inputs:
        flashcard = ReviewItem(study_activity=flashcards_activity)
        session.add(flashcard)

        front = ReviewItemContent(
            content=inp.front,
            type=ReviewItemContentType.FLASHCARDS_FRONT,
            review_item=flashcard,
        )
        back = ReviewItemContent(
            content=inp.back,
            type=ReviewItemContentType.FLASHCARDS_BACK,
            review_item=flashcard,
        )

        session.add(front)
        session.add(back)

    await session.commit()
    # Refetches
    query = (
        select(StudyActivity)
        .where(StudyActivity.id == flashcards_activity_id)
        .options(
            selectinload(
                StudyActivity.review_items.and_(ReviewItem.is_deleted == False)  # type: ignore
            ).selectinload(ReviewItem.contents)  # type: ignore
        )
    )

    result = (await session.execute(query)).scalars().first()

    flashcards_activity = StudyActivityOutputComplete.model_validate(result)

    return flashcards_activity


# ----- READ ----- #


async def read_all_study_activity(
    session: AsyncSession,
    interaction: Interaction,
) -> list[StudyActivity]:
    query = select(StudyActivity).where(
        StudyActivity.interaction_id == interaction.id,
        StudyActivity.is_deleted == False,
    )
    study_activities = (await session.execute(query)).scalars().all()

    return list(study_activities)


async def read_study_activity_complete(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
) -> StudyActivity:

    query = (
        select(StudyActivity)
        .join(Interaction)
        .where(
            StudyActivity.id == study_activity_id,
            Interaction.user_id == user.id,
            StudyActivity.is_deleted == False,
        )
        .options(
            selectinload(
                StudyActivity.review_items.and_(ReviewItem.is_deleted == False)  # type: ignore
            ).selectinload(ReviewItem.contents),  # type: ignore
            selectinload(
                StudyActivity.exercise_items.and_(ExerciseItem.is_deleted == False)  # type: ignore
            ).selectinload(
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
                "is_deleted": False,
            },
        )

    return study_activity


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
        .where(
            StudyActivity.id == study_activity_id,
            Interaction.user_id == user.id,
            StudyActivity.is_deleted == False,
        )
    )

    study_activity = (await session.execute(query)).scalars().first()

    if study_activity is None:
        raise ExceptionNotFound_404(
            "StudyActivity",
            {
                "id": study_activity_id,
                "interaction.user_id": user.id,
                "is_deleted": False,
            },
        )

    update_data = study_activity_update.model_dump(exclude_unset=True)

    study_activity.sqlmodel_update(update_data)

    session.add(study_activity)
    await session.commit()
    await session.refresh(study_activity)

    return study_activity


async def update_flashcard(
    user: User,
    session: AsyncSession,
    flashcard_id: int,
    flashcard_update: FlashcardUpdate,
) -> ReviewItem:
    query = (
        select(ReviewItem)
        .join(StudyActivity)
        .join(Interaction)
        .where(
            ReviewItem.id == flashcard_id,
            ReviewItem.is_deleted == False,
            StudyActivity.activity_format == StudyActivityFormat.FLASHCARDS,
            Interaction.user_id == user.id,
        )
        .options(selectinload(ReviewItem.contents))  # type: ignore
    )

    flashcard = (await session.execute(query)).scalars().first()

    if flashcard is None:
        raise ExceptionNotFound_404(
            "ReviewItem",
            {
                "id": flashcard_id,
                "user_id": user.id,
                "activity_format": StudyActivityFormat.FLASHCARDS.value,
                "is_deleted": False,
            },
        )

    for face in flashcard.contents:
        if face.type == ReviewItemContentType.FLASHCARDS_BACK:
            face.content = flashcard_update.back
        elif face.type == ReviewItemContentType.FLASHCARDS_FRONT:
            face.content = flashcard_update.front

    await session.commit()
    await session.refresh(flashcard, attribute_names=["contents"])

    return flashcard


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
        .where(
            ExerciseItem.id == exercise_item_id,
            Interaction.user_id == user.id,
            ExerciseItem.is_deleted == False,
        )
        .options(selectinload(ExerciseItem.contents))  # type: ignore
    )

    row = (await session.execute(query)).first()

    if row is None:
        raise ExceptionNotFound_404(
            "ExerciseItem",
            {
                "id": exercise_item_id,
                "user_id": user.id,
                "is_deleted": False,
            },
        )

    exercise_item, study_activity = row

    assert isinstance(exercise_item, ExerciseItem)
    assert isinstance(study_activity, StudyActivity)

    if study_activity.is_submitted:
        raise ExceptionSubmittedExercise_409()

    if study_activity.activity_format == StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS:
        if not isinstance(exercise_item_update.attempt, int):
            raise ExceptionRequest_400(
                custom_message="Answers to multiple choice questions need to be an integer pointing to the id of the correct answer."
            )

        # MCQ questions get graded right as they're answered, just not shown
        for content in exercise_item.contents:
            if exercise_item_update.attempt == content.id:
                if content.is_correct:
                    exercise_item.user_score = exercise_item.max_score
                else:
                    exercise_item.user_score = 0
                break
        else:
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

    query = (
        select(ExerciseItem)
        .where(ExerciseItem.id == exercise_item_id)
        .options(selectinload(ExerciseItem.contents))  # type: ignore
    )
    exercise_item = (await session.execute(query)).scalar_one()

    return exercise_item


async def submit_exercise_activity(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
) -> StudyActivityOutputComplete:

    # Fetches study activity
    query = (
        select(StudyActivity, Interaction)
        .join(Interaction)
        .where(
            Interaction.user_id == user.id,
            StudyActivity.id == study_activity_id,
            StudyActivity.activity_type == StudyActivityType.EXERCISE,
            StudyActivity.is_deleted == False,
        )
        .options(
            selectinload(
                StudyActivity.exercise_items.and_(ExerciseItem.is_deleted == False)  # type: ignore
            ).selectinload(
                ExerciseItem.contents  # type: ignore
            ),
        )
    )

    row = (await session.execute(query)).first()

    if row is None:
        raise ExceptionNotFound_404(
            "StudyActivity",
            {
                "id": study_activity_id,
                "user_id": user.id,
                "activity_type": StudyActivityType.EXERCISE.value,
                "is_deleted": False,
            },
        )

    study_activity, interaction = row

    assert isinstance(study_activity, StudyActivity)
    assert isinstance(interaction, Interaction)

    if study_activity.is_submitted:
        raise ExceptionSubmittedExercise_409()

    # Grades if not yet graded
    if study_activity.activity_format == StudyActivityFormat.OPEN_ENDED:
        # === Preparing the json input === #
        questions = OpenEndedGradingInitiationSchema.model_validate(
            {
                "questions_answers": [
                    item.model_dump() for item in study_activity.exercise_items
                ]
            }
        )

        # === Preparing the context document === #
        prompt = "\n".join(item.question for item in study_activity.exercise_items)
        embedded_prompt = await GlobalAPI.embed(prompt)
        document_chunks = await retrieval(
            session=session,
            interaction=interaction,
            raw_prompt=prompt,
            embedded_prompt=embedded_prompt,
        )
        # Temporary close
        await session.commit()

        formatted_chunks = chunks_formatter(document_chunks)

        params = AnswersGradingParams(
            prompt=questions.model_dump_json(),
            creation_prompt=study_activity.prompt,  # type: ignore
            context_document=formatted_chunks,
        )

        final_prompt = answers_grading_augmentation(params)

        # === Grading === #
        i_retry = 0

        while True:
            try:
                grading_results = await GlobalAPI.grade_answers(final_prompt)
                grading_results_python: dict = json.loads(grading_results)
                grading_results_python.update({"grading_input": questions.model_dump()})

                validated_grading_results = OpenEndedGradingResultSchema.model_validate(
                    grading_results_python
                )
                break

            except (ExceptionLLMError_502, ValidationError) as e:
                i_retry += 1
                if i_retry >= settings.N_GENERATION_RETRIES:
                    if isinstance(e, ExceptionLLMError_502):
                        raise
                    else:
                        raise ExceptionLLMError_502(
                            f"Incorrect content format. Details: {e}"
                        )
                continue

    # Refetchs
    query_refetch = (
        select(StudyActivity)
        .where(StudyActivity.id == study_activity_id)
        .options(
            selectinload(
                StudyActivity.review_items.and_(ReviewItem.is_deleted == False)  # type: ignore
            ).selectinload(ReviewItem.contents),  # type: ignore
            selectinload(
                StudyActivity.exercise_items.and_(ExerciseItem.is_deleted == False)  # type: ignore
            ).selectinload(
                ExerciseItem.contents  # type: ignore
            ),
        )
    )
    study_activity = (await session.execute(query_refetch)).scalars().first()

    assert study_activity is not None

    # Updates
    study_activity.is_submitted = True
    study_activity.submitted_at = datetime.now(timezone.utc)

    # Updates item grading if open_ended
    if study_activity.activity_format == StudyActivityFormat.OPEN_ENDED:
        results_map: dict[int, OpenEndedGradingResultItemSchema] = {
            res.id: res for res in validated_grading_results.grading_results
        }

        for exercise_item in study_activity.exercise_items:
            assert exercise_item.id is not None
            graded_result = results_map[exercise_item.id]

            exercise_item.sqlmodel_update(graded_result.model_dump(exclude={"id"}))
            session.add(exercise_item)

    study_activity_output_complete = StudyActivityOutputComplete.model_validate(
        study_activity, context={"show_answers": True}
    )

    await session.commit()

    return study_activity_output_complete


# ----- DELETE ----- #


async def delete_flashcard(
    user: User,
    session: AsyncSession,
    flashcard_id: int,
) -> None:
    query = (
        select(ReviewItem)
        .join(StudyActivity)
        .join(Interaction)
        .where(
            ReviewItem.id == flashcard_id,
            ReviewItem.is_deleted == False,
            StudyActivity.activity_format == StudyActivityFormat.FLASHCARDS,
            Interaction.user_id == user.id,
        )
    )

    flashcard = (await session.execute(query)).scalars().first()

    if flashcard is None:
        raise ExceptionNotFound_404(
            "ReviewItem",
            {
                "id": flashcard_id,
                "user_id": user.id,
                "activity_format": StudyActivityFormat.FLASHCARDS.value,
                "is_deleted": False,
            },
        )

    flashcard.is_deleted = True

    await session.commit()


async def delete_study_activity(
    user: User,
    session: AsyncSession,
    study_activity_id: int,
) -> None:
    query = (
        select(StudyActivity)
        .join(Interaction)
        .where(
            StudyActivity.id == study_activity_id,
            Interaction.user_id == user.id,
            StudyActivity.is_deleted == False,
        )
        .options(
            selectinload(
                StudyActivity.review_items.and_(ReviewItem.is_deleted == False)  # type: ignore
            ),
            selectinload(
                StudyActivity.exercise_items.and_(ExerciseItem.is_deleted == False)  # type: ignore
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
                "is_deleted": False,
            },
        )

    for item in study_activity.items:
        item.is_deleted = True

    subquery_review = select(ReviewItem.id).where(
        ReviewItem.study_activity_id == study_activity_id
    )
    subquery_exercise = select(ExerciseItem.id).where(
        ExerciseItem.study_activity_id == study_activity_id
    )

    query_delete_review_contents = delete(ReviewItemContent).where(
        col(ReviewItemContent.review_item_id).in_(subquery_review)
    )
    query_delete_exercise_contents = delete(ExerciseItemContent).where(
        col(ExerciseItemContent.exercise_item_id).in_(subquery_exercise)
    )

    await session.execute(query_delete_review_contents)
    await session.execute(query_delete_exercise_contents)

    study_activity.is_deleted = True

    await session.commit()
