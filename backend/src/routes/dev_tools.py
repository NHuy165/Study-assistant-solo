from fastapi import APIRouter

from backend.src.core.database import reset_database
from backend.src.core.dependencies import (
    DatetimeDep,
    InteractionDep,
    SessionDep,
    UserDep,
    select,
)
from backend.src.exceptions.core import Responses
from backend.src.models_schema.activity.study_activity import (
    MockStudyActivityInput,
    StudyActivityOutputComplete,
)
from backend.src.services.dev_tools import study_activity

router = APIRouter()


@router.post("/wipe-db", status_code=204)
async def wipe_database():
    await reset_database()


@router.get("/ping", status_code=204)
async def ping(session: SessionDep):
    await session.execute(select(1))


@router.post(
    "/study-activity/{interaction_id}",
    tags=["study-activity"],
    response_model=StudyActivityOutputComplete,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def mock_create_study_activity(
    user: UserDep,
    session: SessionDep,
    current_datetime: DatetimeDep,
    interaction: InteractionDep,
    mock_study_activity_input: MockStudyActivityInput,
):
    """
    Create a study activity with predictable contents, used for testing only.
    """
    return await study_activity.mock_create_study_activity(
        session=session,
        current_datetime=current_datetime,
        interaction=interaction,
        mock_study_activity_input=mock_study_activity_input,
    )


@router.patch(
    "/study-activity/{study_activity_id}/submit",
    tags=["study-activity"],
    response_model=StudyActivityOutputComplete,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
        409: Responses.RESPONSE_409_CONFLICT,
    },
)
async def mock_submit_exercise_activity(
    user: UserDep,
    session: SessionDep,
    current_datetime: DatetimeDep,
    study_activity_id: int,
):
    """
    Nộp tài liệu dạng Exercise.
    """
    unvalidated = await study_activity.mock_submit_exercise_activity(
        user=user,
        session=session,
        current_datetime=current_datetime,
        study_activity_id=study_activity_id,
    )

    study_activity_output_complete = StudyActivityOutputComplete.model_validate(
        unvalidated, context={"show_answers": True}
    )

    return study_activity_output_complete
