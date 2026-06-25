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

# ----- CREATE ----- #


@patch.object(GlobalAPI, "generate_material")
@patch.object(GlobalAPI, "embed")
@patch.object(GlobalAPI, "rewrite_prompt")
@pytest.mark.parametrize(
    "activity_format, subject_type, generated_material, validation_data",
    [
        (
            StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
            SubjectType.MATHS,
            mock_MCQ_llm_return_data,
            validation_MCQ_creation_data,
        ),
        (
            StudyActivityFormat.OPEN_ENDED,
            SubjectType.VIETNAMESE,
            mock_open_ended_llm_return_data,
            validation_open_ended_creation_data,
        ),
        (
            StudyActivityFormat.FLASHCARDS,
            SubjectType.ENGLISH,
            mock_flashcards_llm_return_data,
            validation_flashcards_creation_data,
        ),
        (
            StudyActivityFormat.GAP_FILL,
            SubjectType.ENGLISH,
            mock_gap_fill_llm_return_data,
            validation_gap_fill_creation_data,
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
        f"/api/study-activity/{create_interaction_test.id}",
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
            "prompt": "Study activity generation prompt",
            "activity_type": activity_type,
            "activity_format": study_activity_input.activity_format,
            "subject_type": study_activity_input.subject_type,
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
        f"/api/study-activity/{create_interaction_test.id}/flashcards",
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
                            "type": ReviewItemContentType.FLASHCARDS_FRONT,
                        },
                        {
                            "content": "back 1",
                            "type": ReviewItemContentType.FLASHCARDS_BACK,
                        },
                    ]
                },
                {
                    "contents": [
                        {
                            "content": "front 2",
                            "type": ReviewItemContentType.FLASHCARDS_FRONT,
                        },
                        {
                            "content": "back 2",
                            "type": ReviewItemContentType.FLASHCARDS_BACK,
                        },
                    ]
                },
            ],
        },
    )


# ----- READ ----- #


async def test_read_all_study_activities(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
):
    """
    Reads all study activities.
    """

    # Creates dummy data

    MCQ_dummy = {
        "prompt": "MCQ prompt",
        "activity_format": StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        "subject_type": SubjectType.MATHS,
        "name": "MCQ",
        "is_submitted": False,
    }

    open_ended_dummy = {
        "prompt": "Open ended prompt",
        "activity_format": StudyActivityFormat.OPEN_ENDED,
        "subject_type": SubjectType.VIETNAMESE,
        "name": "Open ended",
        "is_submitted": True,
    }

    flashcards_dummy = {
        "prompt": "Flashcards prompt",
        "activity_format": StudyActivityFormat.FLASHCARDS,
        "subject_type": SubjectType.ENGLISH,
        "name": "Flashcards",
        "is_submitted": False,
    }

    gap_fill_dummy = {
        "prompt": "Gap fill prompt",
        "activity_format": StudyActivityFormat.GAP_FILL,
        "subject_type": SubjectType.ENGLISH,
        "name": "Gap fill",
        "is_submitted": False,
    }

    await create_study_activity_custom(
        **MCQ_dummy,  # type: ignore
        interaction=create_interaction_test,
        is_deleted=False,
    )
    await create_study_activity_custom(
        **open_ended_dummy,  # type: ignore
        interaction=create_interaction_test,
        is_deleted=False,
    )
    await create_study_activity_custom(
        **flashcards_dummy,  # type: ignore
        interaction=create_interaction_test,
        is_deleted=False,
    )
    await create_study_activity_custom(
        **gap_fill_dummy,  # type: ignore
        interaction=create_interaction_test,
        is_deleted=False,
    )

    # Testing

    response = await client.get(
        f"/api/study-activity/{create_interaction_test.id}/",
    )

    validate_status_code(response, 200)
    validate_response_model(response, list[StudyActivityOutput])
    validate_response_contents(
        response,
        [
            MCQ_dummy,
            open_ended_dummy,
            flashcards_dummy,
            gap_fill_dummy,
        ],
    )


@pytest.mark.parametrize(
    "activity_format, subject_type, is_submitted, validation_data",
    [
        (
            StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
            SubjectType.MATHS,
            False,
            validation_MCQ_read_data,
        ),
        (
            StudyActivityFormat.OPEN_ENDED,
            SubjectType.VIETNAMESE,
            True,
            validation_open_ended_read_data,
        ),
        (
            StudyActivityFormat.FLASHCARDS,
            SubjectType.ENGLISH,
            False,
            validation_flashcards_read_data,
        ),
        (
            StudyActivityFormat.GAP_FILL,
            SubjectType.ENGLISH,
            False,
            validation_gap_fill_read_data,
        ),
    ],
)
async def test_read_study_activity_complete(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
    activity_format: StudyActivityFormat,
    subject_type: SubjectType,
    is_submitted: bool,
    validation_data: dict,
):

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        activity_format,
        subject_type,
        "Study activity name",
        is_submitted,
        False,
    )

    response = await client.get(
        f"/api/study-activity/{study_activity.id}/complete",
    )

    validate_status_code(response, 200)
    validate_response_model(response, StudyActivityOutputComplete)
    validate_response_contents(
        response,
        validation_data
        | {
            "name": "Study activity name",
            "prompt": "Study activity creation prompt",
        },
    )


# ----- UPDATE ----- #


async def test_update_study_activity(
    session: AsyncSession,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
):
    """
    Updates a study activity.
    """

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        SubjectType.MATHS,
        "Study activity name",
        True,
        False,
    )

    study_activity_update = StudyActivityUpdate(
        name="Updated name",
        description="Updated description",
    )

    response = await client.patch(
        f"/api/study-activity/{study_activity.id}",
        json=study_activity_update.model_dump(exclude_unset=True),
    )

    validate_status_code(response, 200)
    validate_response_model(response, StudyActivityOutput)
    validate_response_contents(
        response,
        study_activity_update.model_dump(exclude_unset=True),
    )

    # Validates database data
    await session.refresh(study_activity)

    validate_object_contents(
        study_activity,
        study_activity_update.model_dump(exclude_unset=True),
    )


async def test_update_flashcard(
    session: AsyncSession,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
):
    """
    Updates a flashcard in a flashcards study activity.
    """

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        StudyActivityFormat.FLASHCARDS,
        SubjectType.ENGLISH,
        "Study activity name",
        False,
        False,
    )
    flashcard1, flashcard2 = study_activity.review_items

    flashcard_update = FlashcardUpdate(
        front="Updated front",
        back="Updated back",
    )

    response = await client.patch(
        f"/api/study-activity/flashcards/{flashcard1.id}",
        json=flashcard_update.model_dump(exclude_unset=True),
    )

    validate_status_code(response, 200)
    validate_response_model(response, ReviewItemOutput)
    validate_response_contents(
        response,
        {
            "id": flashcard1.id,
            "contents": [
                {
                    "content": "Updated front",
                    "type": ReviewItemContentType.FLASHCARDS_FRONT,
                },
                {
                    "content": "Updated back",
                    "type": ReviewItemContentType.FLASHCARDS_BACK,
                },
            ],
        },
    )

    # Validates database data
    await session.refresh(flashcard1, attribute_names=["contents"])
    await session.refresh(flashcard2, attribute_names=["contents"])

    validate_contents_list(
        [
            {
                "id": flashcard1.id,
                "contents": [content.model_dump() for content in flashcard1.contents],
            },
            {
                "id": flashcard2.id,
                "contents": [content.model_dump() for content in flashcard2.contents],
            },
        ],
        [
            {
                "id": flashcard1.id,
                "contents": [
                    {
                        "content": "Updated front",
                        "type": ReviewItemContentType.FLASHCARDS_FRONT,
                    },
                    {
                        "content": "Updated back",
                        "type": ReviewItemContentType.FLASHCARDS_BACK,
                    },
                ],
            },
            {
                "id": flashcard2.id,
                "contents": [content.model_dump() for content in flashcard2.contents],
            },
        ],
    )


@pytest.mark.parametrize(
    "activity_format, attempt",
    [
        (StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS, 6),
        (
            StudyActivityFormat.OPEN_ENDED,
            "Dummy answer",
        ),
    ],
)
async def test_answer_exercise_item(
    session: AsyncSession,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
    activity_format: StudyActivityFormat,
    attempt: Any,
):
    """
    Answers an exercise item. Also checks for grading if the exercise is a multiple choice.
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

    # Picks question 2 from the exercise, which has not been answered yet.
    question2 = study_activity.exercise_items[1]

    exercise_item_update = ExerciseItemUpdate(
        attempt=attempt,
    )

    response = await client.patch(
        f"/api/study-activity/{question2.id}/answer",
        json=exercise_item_update.model_dump(),
    )

    validate_status_code(response, 200)
    validate_response_model(response, ExerciseItemOutput)
    validate_response_contents(
        response,
        {"attempt": str(attempt)},  # MCQ choice is converted into string in database
    )

    # Validates database data
    await session.refresh(question2)

    validate_object_contents(
        question2,
        {"attempt": str(attempt)},  # MCQ choice is converted into string in database
    )

    # Checks for user score if the exercise is a multiple choice.
    if activity_format == StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS:
        validate_object_contents(
            question2,
            {"user_score": question2.max_score},
        )


@patch.object(GlobalAPI, "embed")
@patch.object(GlobalAPI, "grade_answers")
@pytest.mark.parametrize(
    "activity_format, grading_results_mock",
    [
        (
            StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
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
        ),
        (
            StudyActivityFormat.OPEN_ENDED,
            {
                "grading_results": [
                    {
                        "id": 1,
                        "user_score": settings.DEFAULT_EXERCISE_TOTAL_SCORE / 2,
                        "explanation": "Open ended explanation 1",
                    },
                    {
                        "id": 2,
                        "user_score": 0.0,
                        "explanation": "Open ended explanation 2",
                    },
                ]
            },
        ),
    ],
)
async def test_submit_exercise_activity(
    mock_GlobalAPI_grade_answers: AsyncMock,
    mock_GlobalAPI_embed: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
    activity_format: StudyActivityFormat,
    grading_results_mock: dict,
):
    """
    Submits an exercise (MCQ or open ended).
    """

    # Mock embedding
    mock_GlobalAPI_embed.return_value = [
        0.1
    ] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE

    # Mock answer grading
    mock_GlobalAPI_grade_answers.return_value = json.dumps(grading_results_mock)

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
            "items": grading_results_mock.get("grading_results"),
        },
    )


async def test_delete_study_activity(
    session: AsyncSession,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
):
    """
    Deletes a study activity.
    """

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        SubjectType.MATHS,
        "Study activity name",
        False,
        False,
    )

    response1 = await client.delete(
        f"/api/study-activity/{study_activity.id}",
    )

    validate_status_code(response1, 204)

    response2 = await client.delete(
        f"/api/study-activity/{study_activity.id}",
    )

    validate_status_code(response2, 404)

    # Validates database data
    await session.refresh(study_activity)

    validate_object_contents(study_activity, {"is_deleted": True})


async def test_delete_flashcard(
    session: AsyncSession,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    create_study_activity_custom: Callable[
        [Interaction, str, StudyActivityFormat, SubjectType, str, bool, bool],
        CoroutineType[Any, Any, StudyActivity],
    ],
):
    """
    Deletes a flashcard in a flashcards study activity.
    """

    study_activity = await create_study_activity_custom(
        create_interaction_test,
        "Study activity creation prompt",
        StudyActivityFormat.FLASHCARDS,
        SubjectType.ENGLISH,
        "Study activity name",
        False,
        False,
    )

    flashcard1, flashcard2 = study_activity.review_items

    response1 = await client.delete(f"/api/study-activity/flashcards/{flashcard1.id}")

    validate_status_code(response1, 204)

    response2 = await client.delete(f"/api/study-activity/flashcards/{flashcard1.id}")

    validate_status_code(response2, 404)

    # Validates database data
    await session.refresh(flashcard1)
    await session.refresh(flashcard2)
    await session.refresh(study_activity, attribute_names=["review_items"])

    validate_contents_list(
        [item.model_dump() for item in study_activity.review_items],
        [
            {
                "id": flashcard1.id,
                "is_deleted": True,
            },
            {
                "id": flashcard2.id,
                "is_deleted": False,
            },
        ],
    )
