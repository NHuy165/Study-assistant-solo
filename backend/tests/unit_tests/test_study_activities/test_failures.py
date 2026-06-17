import json
from types import CoroutineType
from typing import Any, Callable
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

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
    ReviewItemOutput,
)
from backend.src.models_schema.activity.study_activity import (
    StudyActivity,
    StudyActivityInput,
    StudyActivityOutputComplete,
)
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    StudyActivityFormat,
    StudyActivityType,
    SubjectType,
)
from backend.src.models_schema.user.user import User
from backend.tests.test_data.study_activities.mock_flashcards_data import (
    mock_flashcards_llm_return_data,
    validation_flashcards_creation_data,
)
from backend.tests.test_data.study_activities.mock_gap_fill_data import (
    mock_gap_fill_llm_return_data,
    validation_gap_fill_creation_data,
)
from backend.tests.test_data.study_activities.mock_MCQ_data import (
    mock_MCQ_llm_return_data,
    validation_MCQ_creation_data,
)
from backend.tests.test_data.study_activities.mock_open_ended_data import (
    mock_open_ended_llm_return_data,
    validation_open_ended_creation_data,
)
from backend.tests.utils.validators import (
    validate_model,
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)

# ----- CREATE ----- #


@patch.object(GlobalAPI, "generate_material")
@patch.object(GlobalAPI, "embed")
@patch.object(GlobalAPI, "rewrite_prompt")
@pytest.mark.parametrize(
    "endpoint_failure",
    [
        ("generate_material"),
        ("embed"),
        ("rewrite_prompt"),
    ],
)
async def test_create_study_activity_failed_api(
    mock_GlobalAPI_rewrite_prompt: AsyncMock,
    mock_GlobalAPI_embed: AsyncMock,
    mock_GlobalAPI_generate_material: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    endpoint_failure: str,
):
    """
    Fails to create an activity due to unavailable external API service.
    """

    # Mock rewrite prompt
    if endpoint_failure == "rewrite_prompt":
        mock_GlobalAPI_rewrite_prompt.side_effect = ExceptionExternalService_503(
            "API failure.",
        )
    else:
        mock_GlobalAPI_rewrite_prompt.return_value = "Mock rewritten prompt"

    # Mock embedding
    if endpoint_failure == "embed":
        mock_GlobalAPI_embed.side_effect = ExceptionExternalService_503(
            "API failure.",
        )
    else:
        mock_GlobalAPI_embed.return_value = [
            0.1
        ] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE

    # Mock study activity generation
    if endpoint_failure == "generate_material":
        mock_GlobalAPI_generate_material.side_effect = ExceptionExternalService_503(
            "API failure.",
        )
    else:
        mock_GlobalAPI_generate_material.return_value = json.dumps(
            mock_MCQ_llm_return_data
        )

    study_activity_input = StudyActivityInput(
        prompt="Study activity generation prompt",
        activity_format=StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        subject_type=SubjectType.MATHS,
    )

    response = await client.post(
        f"/api/study-activity/{create_interaction_test.id}/create",
        json=study_activity_input.model_dump(exclude_unset=True),
    )

    validate_status_code(response, 503)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.EXTERNAL_SERVICE}
    )


@patch.object(GlobalAPI, "generate_material")
@patch.object(GlobalAPI, "embed")
@patch.object(GlobalAPI, "rewrite_prompt")
async def test_create_study_activity_wrong_api_generation(
    mock_GlobalAPI_rewrite_prompt: AsyncMock,
    mock_GlobalAPI_embed: AsyncMock,
    mock_GlobalAPI_generate_material: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
):
    """
    Fails to create an activity due to wrongly formatted generated content.
    """

    # Mock rewrite prompt
    mock_GlobalAPI_rewrite_prompt.return_value = "Mock rewritten prompt"

    # Mock embedding
    mock_GlobalAPI_embed.return_value = [
        0.1
    ] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE

    # Mock study activity generation
    mock_GlobalAPI_generate_material.return_value = json.dumps(
        {
            "wrong_format_content": "wrong_format_content",
        }
    )

    study_activity_input = StudyActivityInput(
        prompt="Study activity generation prompt",
        activity_format=StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        subject_type=SubjectType.MATHS,
    )

    response = await client.post(
        f"/api/study-activity/{create_interaction_test.id}/create",
        json=study_activity_input.model_dump(exclude_unset=True),
    )

    validate_status_code(response, 502)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(response, {"exception_type": ExceptionType.LLM_ERROR})


# ----- UPDATE ----- #


async def test_answer_exercise_item(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
):
    """
    Fails to answer a question in a submitted exercise.
    """

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        StudyActivityFormat.OPEN_ENDED,
        SubjectType.MATHS,
        "Study activity name",
        True,
    )
    question1 = study_activity.exercise_items[0]

    exercise_item_update = ExerciseItemUpdate(attempt="Dummy answer.")

    response = await client.patch(
        f"/api/study-activity/{question1.id}/answer",
        json=exercise_item_update.model_dump(),
    )

    validate_status_code(response, 409)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.SUBMITTED_EXERCISE}
    )


async def test_submit_exercise_activity(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
):
    """
    Fails to submit a submitted exercise.
    """

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        StudyActivityFormat.OPEN_ENDED,
        SubjectType.MATHS,
        "Study activity name",
        True,
    )

    response = await client.patch(
        f"/api/study-activity/{study_activity.id}/submit",
    )

    validate_status_code(response, 409)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.SUBMITTED_EXERCISE}
    )


@patch.object(GlobalAPI, "embed")
@patch.object(GlobalAPI, "grade_answers")
@pytest.mark.parametrize(
    "endpoint_failure",
    [
        ("grade_answers"),
        ("embed"),
    ],
)
async def test_submit_exercise_activity_failed_api(
    mock_GlobalAPI_grade_answers: AsyncMock,
    mock_GlobalAPI_embed: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
    endpoint_failure: str,
):
    """
    Fails to submit an exercise due to unavailable external API service.
    """

    # Mock embedding
    if endpoint_failure == "embed":
        mock_GlobalAPI_embed.side_effect = ExceptionExternalService_503(
            "API failure.",
        )
    else:
        mock_GlobalAPI_embed.return_value = [
            0.1
        ] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE

    # Mock answer grading
    if endpoint_failure == "grade_answers":
        mock_GlobalAPI_grade_answers.side_effect = ExceptionExternalService_503(
            "API failure.",
        )
    else:
        mock_GlobalAPI_grade_answers.return_value = json.dumps(
            {
                "grading_results": [
                    {
                        "id": 1,
                        "explanation": "MCQ explanation 1",
                    },
                    {
                        "id": 2,
                        "explanation": "MCQ explanation 2",
                    },
                ]
            },
        )

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        SubjectType.MATHS,
        "Study activity name",
        False,
    )

    response = await client.patch(
        f"/api/study-activity/{study_activity.id}/submit",
    )

    validate_status_code(response, 503)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.EXTERNAL_SERVICE}
    )


@patch.object(GlobalAPI, "embed")
@patch.object(GlobalAPI, "grade_answers")
async def test_submit_exercise_activity_wrong_api_generation(
    mock_GlobalAPI_grade_answers: AsyncMock,
    mock_GlobalAPI_embed: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
):
    """
    Fails to submit an exercise due to wrongly formatted generated content.
    """

    # Mock embedding
    mock_GlobalAPI_embed.return_value = [
        0.1
    ] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE

    # Mock answer grading
    mock_GlobalAPI_grade_answers.return_value = json.dumps(
        {
            "wrong_format_content": "wrong_format_content",
        },
    )

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        SubjectType.MATHS,
        "Study activity name",
        False,
    )

    response = await client.patch(
        f"/api/study-activity/{study_activity.id}/submit",
    )

    validate_status_code(response, 502)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response,
        {"exception_type": ExceptionType.LLM_ERROR},
    )
