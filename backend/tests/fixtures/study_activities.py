from datetime import datetime, timezone
from types import CoroutineType
from typing import Any, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models_schema.activity.exercise_item import ExerciseItem
from backend.src.models_schema.activity.exercise_item_content import ExerciseItemContent
from backend.src.models_schema.activity.review_item import ReviewItem
from backend.src.models_schema.activity.review_item_content import ReviewItemContent
from backend.src.models_schema.activity.study_activity import StudyActivity
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    ExerciseItemContentType,
    ReviewItemContentType,
    StudyActivityFormat,
    StudyActivityType,
    SubjectType,
)


def create_dummy_MCQ(
    interaction: Interaction,
    prompt: str,
    subject_type: SubjectType,
    name: str,
    is_submitted: bool,
) -> StudyActivity:

    # === Item 1 === #

    choice1_1 = ExerciseItemContent(
        content="Choice 1-1",
        type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
        is_correct=True,
    )

    choice1_2 = ExerciseItemContent(
        content="Choice 1-2",
        type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
        is_correct=False,
    )

    choice1_3 = ExerciseItemContent(
        content="Choice 1-3",
        type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
        is_correct=False,
    )

    choice1_4 = ExerciseItemContent(
        content="Choice 1-4",
        type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
        is_correct=False,
    )

    item1 = ExerciseItem(
        max_score=50,
        question="Question 1",
        user_score=50,
        attempt="1",
        explanation="Explanation 1" if is_submitted else None,
        contents=[choice1_1, choice1_2, choice1_3, choice1_4],
    )

    # === Item 2 === #

    choice2_1 = ExerciseItemContent(
        content="Choice 2-1",
        type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
        is_correct=False,
    )

    choice2_2 = ExerciseItemContent(
        content="Choice 2-2",
        type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
        is_correct=True,
    )

    choice2_3 = ExerciseItemContent(
        content="Choice 2-3",
        type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
        is_correct=False,
    )

    choice2_4 = ExerciseItemContent(
        content="Choice 2-4",
        type=ExerciseItemContentType.MULTIPLE_CHOICE_QUESTIONS_CHOICE,
        is_correct=False,
    )

    item2 = ExerciseItem(
        max_score=50,
        question="Question 2",
        user_score=0,
        attempt=None,
        explanation="Explanation 2" if is_submitted else None,
        contents=[choice2_1, choice2_2, choice2_3, choice2_4],
    )

    # === Activity === #

    study_activity = StudyActivity(
        prompt=prompt,
        activity_type=StudyActivityType.EXERCISE,
        activity_format=StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        subject_type=subject_type,
        name=name,
        description=f"{name}-description",
        is_submitted=is_submitted,
        created_at=datetime.now(timezone.utc),
        submitted_at=datetime.now(timezone.utc) if is_submitted else None,
        interaction=interaction,
        exercise_items=[item1, item2],
    )

    return study_activity


def create_dummy_open_ended(
    interaction: Interaction,
    prompt: str,
    subject_type: SubjectType,
    name: str,
    is_submitted: bool,
) -> StudyActivity:

    # === Item 1 === #

    correct1 = ExerciseItemContent(
        content="Correct answer 1",
        type=ExerciseItemContentType.OPEN_ENDED_CORRECT,
        is_correct=True,
    )

    item1 = ExerciseItem(
        max_score=50,
        question="Question 1",
        user_score=50
        if is_submitted
        else 0,  # Open ended quesiton is only graded after being submitted
        attempt="Answer 1",
        explanation="Explanation 1" if is_submitted else None,
        contents=[correct1],
    )

    # === Item 2 === #

    correct2 = ExerciseItemContent(
        content="Correct answer 2",
        type=ExerciseItemContentType.OPEN_ENDED_CORRECT,
        is_correct=True,
    )

    item2 = ExerciseItem(
        max_score=50,
        question="Question 2",
        user_score=0,
        attempt=None,
        explanation="Explanation 2" if is_submitted else None,
        contents=[correct2],
    )

    # === Activity === #

    study_activity = StudyActivity(
        prompt=prompt,
        activity_type=StudyActivityType.EXERCISE,
        activity_format=StudyActivityFormat.OPEN_ENDED,
        subject_type=subject_type,
        name=name,
        description=f"{name}-description",
        is_submitted=is_submitted,
        created_at=datetime.now(timezone.utc),
        submitted_at=datetime.now(timezone.utc) if is_submitted else None,
        interaction=interaction,
        exercise_items=[item1, item2],
    )

    return study_activity


def create_dummy_flashcards(
    interaction: Interaction,
    prompt: str,
    subject_type: SubjectType,
    name: str,
) -> StudyActivity:

    # === Item 1 === #

    front1 = ReviewItemContent(
        content="Flashcard front 1",
        type=ReviewItemContentType.FLASHCARDS_FRONT,
    )
    back1 = ReviewItemContent(
        content="Flashcard back 1",
        type=ReviewItemContentType.FLASHCARDS_BACK,
    )

    item1 = ReviewItem(contents=[front1, back1])

    # === Item 2 === #

    front2 = ReviewItemContent(
        content="Flashcard front 2",
        type=ReviewItemContentType.FLASHCARDS_FRONT,
    )
    back2 = ReviewItemContent(
        content="Flashcard back 2",
        type=ReviewItemContentType.FLASHCARDS_BACK,
    )

    item2 = ReviewItem(contents=[front2, back2])

    # === Activity === #

    study_activity = StudyActivity(
        prompt=prompt,
        activity_type=StudyActivityType.REVIEW,
        activity_format=StudyActivityFormat.FLASHCARDS,
        subject_type=subject_type,
        name=name,
        description=f"{name}-description",
        created_at=datetime.now(timezone.utc),
        interaction=interaction,
        review_items=[item1, item2],
    )

    return study_activity


def create_dummy_gap_fill(
    interaction: Interaction,
    prompt: str,
    subject_type: SubjectType,
    name: str,
) -> StudyActivity:

    # === Item 1 === #

    text1 = ReviewItemContent(
        content="Text 1: $!BLANK!$ - $!BLANK!$",
        type=ReviewItemContentType.GAP_FILL_TEXT,
    )
    correct1_1 = ReviewItemContent(
        content="Correct 1-1",
        type=ReviewItemContentType.GAP_FILL_CORRECT,
    )
    correct1_2 = ReviewItemContent(
        content="Correct 1-2",
        type=ReviewItemContentType.GAP_FILL_CORRECT,
    )
    distractor1_1 = ReviewItemContent(
        content="Distractor 1-1",
        type=ReviewItemContentType.GAP_FILL_DISTRACTOR,
    )
    distractor1_2 = ReviewItemContent(
        content="Distractor 1-2",
        type=ReviewItemContentType.GAP_FILL_DISTRACTOR,
    )

    item1 = ReviewItem(
        contents=[text1, correct1_1, correct1_2, distractor1_1, distractor1_2]
    )

    # === Item 2 === #

    text2 = ReviewItemContent(
        content="Text 2: $!BLANK!$ - $!BLANK!$",
        type=ReviewItemContentType.GAP_FILL_TEXT,
    )
    correct2_1 = ReviewItemContent(
        content="Correct 2-1",
        type=ReviewItemContentType.GAP_FILL_CORRECT,
    )
    correct2_2 = ReviewItemContent(
        content="Correct 2-2",
        type=ReviewItemContentType.GAP_FILL_CORRECT,
    )
    distractor2_1 = ReviewItemContent(
        content="Distractor 2-1",
        type=ReviewItemContentType.GAP_FILL_DISTRACTOR,
    )
    distractor2_2 = ReviewItemContent(
        content="Distractor 2-2",
        type=ReviewItemContentType.GAP_FILL_DISTRACTOR,
    )

    item2 = ReviewItem(
        contents=[text2, correct2_1, correct2_2, distractor2_1, distractor2_2]
    )

    # === Activity === #

    study_activity = StudyActivity(
        prompt=prompt,
        activity_type=StudyActivityType.REVIEW,
        activity_format=StudyActivityFormat.GAP_FILL,
        subject_type=subject_type,
        name=name,
        description=f"{name}-description",
        created_at=datetime.now(timezone.utc),
        interaction=interaction,
        review_items=[item1, item2],
    )

    return study_activity


@pytest.fixture(name="create_study_activity_custom")
async def create_study_activity_custom_fixture(
    session: AsyncSession,
) -> Callable[
    [Interaction, str, StudyActivityFormat, SubjectType, str, bool],
    CoroutineType[Any, Any, StudyActivity],
]:
    """
    Returns a function that creates a custom study activity attached to an interaction
    """

    async def create_llm_response_custom(
        interaction: Interaction,
        prompt: str,
        activity_format: StudyActivityFormat,
        subject_type: SubjectType,
        name: str,
        is_submitted: bool,
    ) -> StudyActivity:

        if activity_format == StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS:
            study_activity = create_dummy_MCQ(
                interaction=interaction,
                prompt=prompt,
                subject_type=subject_type,
                name=name,
                is_submitted=is_submitted,
            )
        elif activity_format == StudyActivityFormat.OPEN_ENDED:
            study_activity = create_dummy_open_ended(
                interaction=interaction,
                prompt=prompt,
                subject_type=subject_type,
                name=name,
                is_submitted=is_submitted,
            )
        elif activity_format == StudyActivityFormat.FLASHCARDS:
            study_activity = create_dummy_flashcards(
                interaction=interaction,
                prompt=prompt,
                subject_type=subject_type,
                name=name,
            )
        else:
            study_activity = create_dummy_gap_fill(
                interaction=interaction,
                prompt=prompt,
                subject_type=subject_type,
                name=name,
            )

        session.add(study_activity)
        await session.commit()

        return study_activity

    return create_llm_response_custom
