from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from backend.src.exceptions.core import (
    ExceptionNotFound_404,
    ExceptionSubmittedExercise_409,
)
from backend.src.models_schema.activity.exercise_item import (
    ExerciseItem,
)
from backend.src.models_schema.activity.llm_return_json_schema import (
    FlashcardItemSchema,
    FlashcardsCreationSchema,
    MCQCreationSchema,
    MCQItemSchema,
    OpenEndedCreationSchema,
    OpenEndedItemSchema,
)
from backend.src.models_schema.activity.study_activity import (
    MockStudyActivityInput,
    StudyActivity,
)
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    StudyActivityFormat,
    StudyActivityType,
)
from backend.src.models_schema.user.user import User
from backend.src.services.study_activity import (
    save_flashcards,
    save_multiple_choice_questions,
    save_open_ended,
)


async def mock_create_study_activity(
    session: AsyncSession,
    current_datetime: datetime,
    interaction: Interaction,
    mock_study_activity_input: MockStudyActivityInput,
) -> StudyActivity:
    """
    Creates mock data with predictable contents.
    """

    # ----- Study activity initiation ----- #
    if mock_study_activity_input.activity_format in (
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        StudyActivityFormat.OPEN_ENDED,
    ):
        activity_type = StudyActivityType.EXERCISE
    else:
        activity_type = StudyActivityType.REVIEW

    study_activity = StudyActivity(
        prompt=mock_study_activity_input.prompt,
        activity_type=activity_type,
        activity_format=mock_study_activity_input.activity_format,
        subject_type=mock_study_activity_input.subject_type,
        name=mock_study_activity_input.name,
        description=mock_study_activity_input.description,
        interaction=interaction,
        created_at=current_datetime,
    )

    # ----- Items generation and saving ----- #

    items_list = []
    # === Multiple choice questions === #

    if (
        mock_study_activity_input.activity_format
        == StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS
    ):
        # Generates items
        for i in range(mock_study_activity_input.n_items):
            item = MCQItemSchema(
                question=f"Test question {i + 1}",
                answers=[f"Test choice {i + 1}-{j}" for j in range(1, 5)],
                correct=i % 4,
            )
            items_list.append(item)
        activity_data = MCQCreationSchema(
            name=mock_study_activity_input.name,
            description=mock_study_activity_input.description,
            activity_items=items_list,
        )

        # Saves
        save_multiple_choice_questions(
            activity_data=activity_data, study_activity=study_activity
        )

    # === Open ended === #
    elif mock_study_activity_input.activity_format == StudyActivityFormat.OPEN_ENDED:
        # Generates items
        for i in range(mock_study_activity_input.n_items):
            item = OpenEndedItemSchema(
                question=f"Test question {i + 1}",
                correct=f"Test correct answer {i + 1}",
            )
            items_list.append(item)
        activity_data = OpenEndedCreationSchema(
            name=mock_study_activity_input.name,
            description=mock_study_activity_input.description,
            activity_items=items_list,
        )

        # Saves
        save_open_ended(activity_data=activity_data, study_activity=study_activity)

    # === Flashcards === #
    else:
        # Generates items
        for i in range(mock_study_activity_input.n_items):
            item = FlashcardItemSchema(
                front=f"Test front {i + 1}",
                back=f"Test back {i + 1}",
            )
            items_list.append(item)
        activity_data = FlashcardsCreationSchema(
            name=mock_study_activity_input.name,
            description=mock_study_activity_input.description,
            activity_items=items_list,
        )

        # Saves
        save_flashcards(activity_data=activity_data, study_activity=study_activity)

    session.add(study_activity)
    await session.commit()

    return study_activity


async def mock_submit_exercise_activity(
    user: User,
    session: AsyncSession,
    current_datetime: datetime,
    study_activity_id: int,
) -> StudyActivity:

    # === Fetches and sets up the study activity === #
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

    # Checks for submission status
    if study_activity.is_submitted:
        raise ExceptionSubmittedExercise_409()

    # === Grading / explaining the questions and answers === #

    for exercise_item in study_activity.exercise_items:
        # MCQ only needs the explanation
        if (
            study_activity.activity_format
            == StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS
        ):
            pass

        # Open ended: Any answer that is not null or blank will be scored using maximum score.
        else:
            if exercise_item.attempt is not None and len(exercise_item.attempt) > 0:
                exercise_item.user_score = exercise_item.max_score

        exercise_item.explanation = f"{exercise_item.question}: {'WRONG' if exercise_item.user_score == 0 else 'CORRECT'}"

    # === Updates status and returns === #
    study_activity.is_submitted = True
    study_activity.submitted_at = current_datetime

    await session.commit()

    study_activity.exercise_items.sort(key=lambda x: x.id if x.id else 0)

    for item in study_activity.exercise_items:
        item.contents.sort(key=lambda x: x.id if x.id else 0)

    return study_activity
