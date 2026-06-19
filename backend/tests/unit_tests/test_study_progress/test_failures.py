import json
import time
from datetime import date, datetime, timedelta, timezone
from types import CoroutineType, NoneType
from typing import Any, Callable
from unittest.mock import AsyncMock, patch

import pytest
import time_machine
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.ai_api import GlobalAPI
from backend.src.core.config import settings
from backend.src.exceptions.core import (
    ExceptionExternalService_503,
    ExceptionResponse,
    ExceptionType,
)
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
    AggregateTarget,
    CriterionAttribute,
    ExerciseItemContentType,
    OperatorType,
    ReviewItemContentType,
    StudyActivityFormat,
    StudyActivityType,
    SubjectType,
)
from backend.src.models_schema.study_progress.assessment import (
    StudyAssessment,
    StudyAssessmentOutput,
)
from backend.src.models_schema.study_progress.criterion import Criterion
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


@patch.object(GlobalAPI, "generate_study_assessment")
async def test_create_study_assessment_failed_api(
    mock_GlobalAPI_generate_study_assessment: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
):
    """
    Fails to create a study assessment due to unavailable external API service.
    """

    # Mock study assessment generation
    mock_GlobalAPI_generate_study_assessment.side_effect = ExceptionExternalService_503(
        "API failure.",
    )

    today = datetime.now(timezone.utc).date()
    with time_machine.travel(today + timedelta(days=1)):
        response = await client.post(
            "/api/study-progress/study-assessment",
        )

    validate_status_code(response, 503)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.EXTERNAL_SERVICE}
    )


@pytest.mark.parametrize(
    "criteria",
    [
        # Wrong value with subject_type attribute
        [
            {
                "attribute": CriterionAttribute.SUBJECT_TYPE,
                "value": "wrong_string",
                "operator": OperatorType.EQ,
            },
        ],
        # Wrong value with activity_type attribute
        [
            {
                "attribute": CriterionAttribute.ACTIVITY_TYPE,
                "value": "wrong_string",
                "operator": OperatorType.EQ,
            },
        ],
        # Wrong value with activity_format attribute
        [
            {
                "attribute": CriterionAttribute.ACTIVITY_FORMAT,
                "value": "wrong_string",
                "operator": OperatorType.EQ,
            },
        ],
        # Wrong date value (format)
        [
            {
                "attribute": CriterionAttribute.CREATED_AT,
                "value": "15/05/2000",
                "operator": OperatorType.EQ,
            },
        ],
        # Wrong date value (format)
        [
            {
                "attribute": CriterionAttribute.SUBMITTED_AT,
                "value": "15/05/2000",
                "operator": OperatorType.EQ,
            },
        ],
        # Wrong operator with is_submitted attribute
        [
            {
                "attribute": CriterionAttribute.IS_SUBMITTED,
                "value": True,
                "operator": OperatorType.LE,
            },
        ],
        # Wrong value with is_submitted attribute
        [
            {
                "attribute": CriterionAttribute.IS_SUBMITTED,
                "value": 5,
                "operator": OperatorType.EQ,
            },
        ],
        # Wrong value with interaction_id attribute
        [
            {
                "attribute": CriterionAttribute.INTERACTION_ID,
                "value": "wrong_string",
                "operator": OperatorType.EQ,
            },
        ],
    ],
)
async def test_get_study_progress(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
    criteria: list[dict],
):
    """
    Tests auto validations of the Criterion class.
    """

    response = await client.post(
        f"/api/study-progress?target={AggregateTarget.COUNT_ACTIVITY}",
        json=criteria,
    )

    validate_status_code(response, 400)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.REQUEST_VALIDATION}
    )
