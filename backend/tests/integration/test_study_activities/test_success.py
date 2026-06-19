import json
from types import CoroutineType
from typing import Any, Callable
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.ai_api import GlobalAPI
from backend.src.core.config import settings
from backend.src.models_schema.activity.exercise_item import (
    ExerciseItemOutput,
    ExerciseItemUpdate,
)
from backend.src.models_schema.activity.review_item import (
    FlashcardInput,
    FlashcardUpdate,
    ReviewItemOutput,
)
from backend.src.models_schema.activity.study_activity import (
    FlashcardsActivityInput,
    StudyActivity,
    StudyActivityInput,
    StudyActivityOutput,
    StudyActivityOutputComplete,
    StudyActivityUpdate,
)
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    ExerciseItemContentType,
    ReviewItemContentType,
    StudyActivityFormat,
    StudyActivityType,
    SubjectType,
)
from backend.src.models_schema.user.user import User
from backend.tests.test_data.study_activities.mock_flashcards_data import (
    mock_flashcards_llm_return_data,
    validation_flashcards_creation_data,
    validation_flashcards_read_data,
)
from backend.tests.test_data.study_activities.mock_gap_fill_data import (
    mock_gap_fill_llm_return_data,
    validation_gap_fill_creation_data,
    validation_gap_fill_read_data,
)
from backend.tests.test_data.study_activities.mock_MCQ_data import (
    mock_MCQ_llm_return_data,
    validation_MCQ_creation_data,
    validation_MCQ_read_data,
)
from backend.tests.test_data.study_activities.mock_open_ended_data import (
    mock_open_ended_llm_return_data,
    validation_open_ended_creation_data,
    validation_open_ended_read_data,
)
from backend.tests.utils.validators import (
    validate_contents_dict,
    validate_contents_list,
    validate_model,
    validate_object_contents,
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)


@pytest.mark.skipif(
    not settings.RUN_INTEGRATION, reason="Auto skipping integration tests."
)
@pytest.mark.integration
@pytest.mark.parametrize(
    "activity_format, subject_type",
    [
        (
            StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
            SubjectType.MATHS,
        ),
        (
            StudyActivityFormat.OPEN_ENDED,
            SubjectType.VIETNAMESE,
        ),
        (
            StudyActivityFormat.FLASHCARDS,
            SubjectType.ENGLISH,
        ),
        (
            StudyActivityFormat.GAP_FILL,
            SubjectType.ENGLISH,
        ),
    ],
)
async def test_create_study_activity(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    activity_format: StudyActivityFormat,
    subject_type: SubjectType,
):
    """
    Tests all API calls in a study activity creation process.
    """

    study_activity_input = StudyActivityInput(
        prompt="Hãy cho tôi 5 câu.",
        activity_format=activity_format,
        subject_type=subject_type,
    )

    response = await client.post(
        f"/api/study-activity/{create_interaction_test.id}/create",
        json=study_activity_input.model_dump(exclude_unset=True),
    )

    if study_activity_input.activity_format in (
        StudyActivityFormat.FLASHCARDS,
        StudyActivityFormat.GAP_FILL,
    ):
        activity_type = StudyActivityType.REVIEW
    else:
        activity_type = StudyActivityType.EXERCISE

    validate_status_code(response, 200)
    validate_response_model(response, StudyActivityOutputComplete)
    validate_model(
        response.json().get("items"),
        list[ReviewItemOutput]
        if activity_type == StudyActivityType.REVIEW
        else list[ExerciseItemOutput],
    )
    validate_response_contents(
        response,
        {
            "prompt": "Hãy cho tôi 5 câu.",
            "activity_type": activity_type,
            "activity_format": study_activity_input.activity_format,
            "subject_type": study_activity_input.subject_type,
            "is_submitted": False,
            "submitted_at": None,
        },
    )


@pytest.mark.skipif(
    not settings.RUN_INTEGRATION, reason="Auto skipping integration tests."
)
@pytest.mark.integration
@pytest.mark.parametrize(
    "activity_format",
    [
        (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS),
        (StudyActivityFormat.OPEN_ENDED),
    ],
)
async def test_submit_exercise_activity(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
    activity_format: StudyActivityFormat,
):
    """
    Tests all API calls in an exercise submission and grading process
    """

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        activity_format,
        SubjectType.MATHS,
        "Study activity name",
        False,
        False,
    )

    response = await client.patch(
        f"/api/study-activity/{study_activity.id}/submit",
    )

    validate_status_code(response, 200)
    validate_response_model(response, StudyActivityOutputComplete)
    validate_response_contents(
        response,
        {
            "id": study_activity.id,
            "is_submitted": True,
        },
    )
