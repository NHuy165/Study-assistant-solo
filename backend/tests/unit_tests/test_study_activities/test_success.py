import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from backend.src.core.ai_api import GlobalAPI
from backend.src.core.config import settings
from backend.src.models_schema.activity.exercise_item import ExerciseItemOutput
from backend.src.models_schema.activity.review_item import (
    FlashcardInput,
    ReviewItemOutput,
)
from backend.src.models_schema.activity.study_activity import (
    FlashcardsActivityInput,
    StudyActivityInput,
    StudyActivityOutput,
    StudyActivityOutputComplete,
)
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    ReviewItemContentType,
    StudyActivityFormat,
    StudyActivityType,
    SubjectType,
)
from backend.src.models_schema.user.user import User
from backend.tests.test_data.study_activities.mock_flashcards_data import (
    mock_flashcards_data,
    validation_flashcards_data,
)
from backend.tests.test_data.study_activities.mock_gap_fill_data import (
    mock_gap_fill_data,
    validation_gap_fill_data,
)
from backend.tests.test_data.study_activities.mock_MCQ_data import (
    mock_MCQ_data,
    validation_MCQ_data,
)
from backend.tests.test_data.study_activities.mock_open_ended_data import (
    mock_open_ended_data,
    validation_open_ended_data,
)
from backend.tests.utils.validators import (
    validate_model,
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)


@patch.object(GlobalAPI, "generate_material")
@patch.object(GlobalAPI, "embed")
@patch.object(GlobalAPI, "rewrite_prompt")
@pytest.mark.parametrize(
    "activity_format, subject_type, generated_material, validation_data",
    [
        (
            StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
            SubjectType.MATHS,
            mock_MCQ_data,
            validation_MCQ_data,
        ),
        (
            StudyActivityFormat.OPEN_ENDED,
            SubjectType.VIETNAMESE,
            mock_open_ended_data,
            validation_open_ended_data,
        ),
        (
            StudyActivityFormat.FLASHCARDS,
            SubjectType.ENGLISH,
            mock_flashcards_data,
            validation_flashcards_data,
        ),
        (
            StudyActivityFormat.GAP_FILL,
            SubjectType.ENGLISH,
            mock_gap_fill_data,
            validation_gap_fill_data,
        ),
    ],
)
async def test_create_study_activity(
    mock_GlobalAPI_rewrite_prompt: AsyncMock,
    mock_GlobalAPI_embed: AsyncMock,
    mock_GlobalAPI_generate_material: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    activity_format: StudyActivityFormat,
    subject_type: SubjectType,
    generated_material: dict,
    validation_data: list,
):
    """
    Creates an MCQ, open ended, flashcards and gap fill study activity of various subjects.
    """

    # Mock rewrite prompt
    mock_GlobalAPI_rewrite_prompt.return_value = "Mock rewritten prompt"

    # Mock embedding
    mock_GlobalAPI_embed.return_value = [
        0.1
    ] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE

    # Mock study activity generation
    mock_GlobalAPI_generate_material.return_value = json.dumps(generated_material)

    study_activity_input = StudyActivityInput(
        prompt="Study activity generation prompt",
        activity_format=activity_format,
        subject_type=subject_type,
    )

    response = await client.post(
        f"/api/study-activity/{create_interaction_test.id}/create",
        json=study_activity_input.model_dump(exclude_unset=True),
    )

    validate_status_code(response, 200)
    validate_response_model(response, StudyActivityOutputComplete)
    validate_model(
        response.json().get("items"),
        list[ReviewItemOutput]
        if study_activity_input.activity_type == StudyActivityType.REVIEW
        else list[ExerciseItemOutput],
    )
    validate_response_contents(
        response,
        {
            "prompt": "Study activity generation prompt",
            "activity_type": study_activity_input.activity_type.value,  # type: ignore
            "activity_format": study_activity_input.activity_format.value,
            "subject_type": study_activity_input.subject_type.value,
            "is_submitted": False,
            "submitted_at": None,
            "items": validation_data,
        },
    )


async def test_create_add_flashcards_activity(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
):
    """
    Creates a flashcard activity and adds flashcards the manual way.
    """

    # === Creates the activity === #
    flashcards_activity_input = FlashcardsActivityInput(
        subject_type=SubjectType.ENGLISH,
        name="Flashcards name",
        description="Flashcards description",
    )

    response_create = await client.post(
        f"/api/study-activity/{create_interaction_test.id}/flashcards/create",
        json=flashcards_activity_input.model_dump(),
    )

    validate_status_code(response_create, 200)
    validate_response_model(response_create, StudyActivityOutput)
    validate_response_contents(
        response_create,
        flashcards_activity_input.model_dump()
        | {
            "prompt": None,
            "activity_type": StudyActivityType.REVIEW.value,
            "activity_format": StudyActivityFormat.FLASHCARDS.value,
        },
    )

    # === Adds the flashcards === #
    flashcard1 = FlashcardInput(front="front 1", back="back 1")
    flashcard2 = FlashcardInput(front="front 2", back="back 2")
    flashcards_to_add = [
        flashcard1.model_dump(),
        flashcard2.model_dump(),
    ]

    response_add = await client.post(
        f"/api/study-activity/{response_create.json().get('id')}/add-cards",
        json=flashcards_to_add,
    )

    validate_status_code(response_add, 200)
    validate_response_model(response_add, StudyActivityOutputComplete)
    validate_response_contents(
        response_add,
        {
            "id": response_create.json().get("id"),
            "items": [
                {
                    "contents": [
                        {
                            "content": "front 1",
                            "type": ReviewItemContentType.FLASHCARDS_FRONT.value,
                        },
                        {
                            "content": "back 1",
                            "type": ReviewItemContentType.FLASHCARDS_BACK.value,
                        },
                    ]
                },
                {
                    "contents": [
                        {
                            "content": "front 2",
                            "type": ReviewItemContentType.FLASHCARDS_FRONT.value,
                        },
                        {
                            "content": "back 2",
                            "type": ReviewItemContentType.FLASHCARDS_BACK.value,
                        },
                    ]
                },
            ],
        },
    )
