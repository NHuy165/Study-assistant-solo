from datetime import datetime, timedelta, timezone

import pytest
import time_machine
from httpx import AsyncClient

from backend.src.core.config import settings
from backend.src.models_schema.study_progress.assessment import (
    StudyAssessmentOutput,
)
from backend.src.models_schema.user.user import User
from backend.tests.utils.validators import (
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)

# ----- CREATE ----- #


@pytest.mark.skipif(
    not settings.RUN_INTEGRATION, reason="Auto skipping integration tests."
)
@pytest.mark.integration
async def test_create_study_assessment(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
):
    """
    Tests all API calls in a study assessment creation process.
    """

    today = datetime.now(timezone.utc).date()
    with time_machine.travel(today + timedelta(days=1)):
        response = await client.post(
            "/api/study-progress/study-assessment",
        )

    validate_status_code(response, 200)
    validate_response_model(response, list[StudyAssessmentOutput])
    validate_response_contents(
        response,
        [
            {
                "assessment_of": today.isoformat(),
            },
        ],
    )
