from types import CoroutineType
from typing import Any, Callable

from httpx import AsyncClient

from backend.src.exceptions.core import ExceptionResponse, ExceptionType
from backend.src.models_schema.activity.exercise_item import ExerciseItemUpdate
from backend.src.models_schema.activity.study_activity import StudyActivity
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    StudyActivityFormat,
    SubjectType,
)
from backend.src.models_schema.user.user import User
from backend.tests.utils.validators import (
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)


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
