from datetime import date, datetime, timedelta, timezone
from types import CoroutineType, NoneType
from typing import Any, Callable
from unittest.mock import AsyncMock, patch

import pytest
import time_machine
from httpx import AsyncClient

from backend.src.core.ai_api import GlobalAPI
from backend.src.models_schema.activity.study_activity import (
    StudyActivity,
)
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    AggregateTarget,
    StudyActivityFormat,
    SubjectType,
)
from backend.src.models_schema.study_progress.assessment import (
    StudyAssessment,
    StudyAssessmentOutput,
)
from backend.src.models_schema.study_progress.criterion import Criterion
from backend.src.models_schema.user.user import User
from backend.tests.test_data.study_progress import test_cases_data
from backend.tests.utils.validators import (
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)

# ----- CREATE ----- #


@patch.object(GlobalAPI, "generate_study_assessment")
async def test_create_study_assessment(
    mock_GlobalAPI_generate_study_assessment: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
):
    """
    Creates a study assessment.
    """

    # Mock study assessment generation
    mock_GlobalAPI_generate_study_assessment.return_value = "Mock study assessment"

    response_today = await client.post(
        "/api/study-progress/study-assessment",
    )

    validate_status_code(response_today, 200)
    validate_response_model(response_today, NoneType)

    today = datetime.now(timezone.utc).date()
    with time_machine.travel(today + timedelta(days=1)):
        response_tomorrow = await client.post(
            "/api/study-progress/study-assessment",
        )

    validate_status_code(response_tomorrow, 200)
    validate_response_model(response_tomorrow, StudyAssessmentOutput)
    validate_response_contents(
        response_tomorrow,
        {
            "content": "Mock study assessment",
            "assessment_of": today.isoformat(),
        },
    )


# ----- READ ----- #

# === Study assessment === #


async def test_read_study_assessments(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_study_assessment_custom: Callable[
        [User, date, datetime | None], CoroutineType[Any, Any, StudyAssessment]
    ],
):
    """
    Reads all study assessments with and without filters.
    """

    today = datetime.now(timezone.utc).date()
    today_prev_1 = today - timedelta(days=1)
    today_prev_2 = today - timedelta(days=2)
    today_prev_3 = today - timedelta(days=3)

    await create_study_assessment_custom(register_user_test, today_prev_1, None)
    await create_study_assessment_custom(register_user_test, today_prev_2, None)
    await create_study_assessment_custom(register_user_test, today_prev_3, None)

    # Reads all
    response_all = await client.get(
        "/api/study-progress/study-assessment",
    )

    validate_status_code(response_all, 200)
    validate_response_model(response_all, list[StudyAssessmentOutput])
    validate_response_contents(
        response_all,
        [
            {
                "assessment_of": today_prev_1.isoformat(),
                "content": f"Study assessment of {today_prev_1.isoformat()}",
            },
            {
                "assessment_of": today_prev_2.isoformat(),
                "content": f"Study assessment of {today_prev_2.isoformat()}",
            },
            {
                "assessment_of": today_prev_3.isoformat(),
                "content": f"Study assessment of {today_prev_3.isoformat()}",
            },
        ],
    )

    # Reads with a limit of 2
    response_limit_2 = await client.get(
        "/api/study-progress/study-assessment?limit=2",
    )

    validate_status_code(response_limit_2, 200)
    validate_response_model(response_limit_2, list[StudyAssessmentOutput])
    validate_response_contents(
        response_limit_2,
        [
            {
                "assessment_of": today_prev_1.isoformat(),
                "content": f"Study assessment of {today_prev_1.isoformat()}",
            },
            {
                "assessment_of": today_prev_2.isoformat(),
                "content": f"Study assessment of {today_prev_2.isoformat()}",
            },
        ],
    )

    # Reads with a limit of 2 and an offset of 1
    response_limit_2_offset_1 = await client.get(
        "/api/study-progress/study-assessment?offset=1&limit=2",
    )

    validate_status_code(response_limit_2_offset_1, 200)
    validate_response_model(response_limit_2_offset_1, list[StudyAssessmentOutput])
    validate_response_contents(
        response_limit_2_offset_1,
        [
            {
                "assessment_of": today_prev_2.isoformat(),
                "content": f"Study assessment of {today_prev_2.isoformat()}",
            },
            {
                "assessment_of": today_prev_3.isoformat(),
                "content": f"Study assessment of {today_prev_3.isoformat()}",
            },
        ],
    )


async def test_read_study_assessment_one(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_study_assessment_custom: Callable[
        [User, date, datetime | None], CoroutineType[Any, Any, StudyAssessment]
    ],
):
    """
    Reads the latest study assessment.
    Reads a study assessment by date.
    """

    today = datetime.now(timezone.utc).date()
    today_prev_1 = today - timedelta(days=1)
    today_prev_2 = today - timedelta(days=2)
    today_prev_3 = today - timedelta(days=3)

    await create_study_assessment_custom(register_user_test, today_prev_1, None)
    await create_study_assessment_custom(register_user_test, today_prev_2, None)
    await create_study_assessment_custom(register_user_test, today_prev_3, None)

    # Reads the latest study assessment
    response_latest = await client.get(
        "/api/study-progress/study-assessment/latest",
    )

    validate_status_code(response_latest, 200)
    validate_response_model(response_latest, StudyAssessmentOutput)
    validate_response_contents(
        response_latest,
        {
            "assessment_of": today_prev_1.isoformat(),
            "content": f"Study assessment of {today_prev_1.isoformat()}",
        },
    )

    # Reads a study assessment by date
    response_by_date = await client.get(
        f"/api/study-progress/study-assessment/by-date?specific_date={today_prev_2.isoformat()}",
    )

    validate_status_code(response_by_date, 200)
    validate_response_model(response_by_date, StudyAssessmentOutput)
    validate_response_contents(
        response_by_date,
        {
            "assessment_of": today_prev_2.isoformat(),
            "content": f"Study assessment of {today_prev_2.isoformat()}",
        },
    )


# === Study progress === #


@pytest.mark.parametrize(
    "target, criteria, validation",
    [
        (
            test_cases_data.target_1,
            test_cases_data.criteria_1,
            test_cases_data.validation_1,
        ),
        (
            test_cases_data.target_2,
            test_cases_data.criteria_2,
            test_cases_data.validation_2,
        ),
        (
            test_cases_data.target_3,
            test_cases_data.criteria_3,
            test_cases_data.validation_3,
        ),
        (
            test_cases_data.target_4,
            test_cases_data.criteria_4,
            test_cases_data.validation_4,
        ),
        (
            test_cases_data.target_5,
            test_cases_data.criteria_5,
            test_cases_data.validation_5,
        ),
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
    target: AggregateTarget,
    criteria: list[Criterion],
    validation: list,
):
    """
    Tests various scenarios of using the study progress endpoint.
    Detailed test cases can be seen in test_data/study_progress
    """

    # Creates data
    for (
        activity_format,
        subject_type,
        is_deleted,
        is_submitted,
    ) in test_cases_data.study_activities:
        await create_study_activity_custom(
            create_interaction_test,
            "Dummy prompt",
            activity_format,
            subject_type,
            "Study activity",
            is_submitted,
            is_deleted,
        )

    response = await client.post(
        f"/api/study-progress?target={target.value}",
        json=[criterion.model_dump() for criterion in criteria],
    )

    validate_status_code(response, 200)
    validate_response_model(response, list[tuple])
    validate_response_contents(response, validation)
