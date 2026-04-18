from fastapi import APIRouter

from backend.src.core.dependencies import InteractionDep, SessionDep, UserDep
from backend.src.models_schema.activity.exercise_activity import ExerciseActivityInput
from backend.src.models_schema.activity.review_activity import ReviewActivityInput
from backend.src.models_schema.activity.study_activity import StudyActivityInput
from backend.src.services.study_activity import create_study_activity

router = APIRouter()


@router.post("/{interaction_id}")
async def test(
    user: UserDep,
    session: SessionDep,
    interaction: InteractionDep,
    study_activity_input: StudyActivityInput,
    review_activity_input: ReviewActivityInput | None = None,
    exercise_activity_input: ExerciseActivityInput | None = None,
):
    return await create_study_activity(
        session,
        interaction,
        study_activity_input,
        review_activity_input,
        exercise_activity_input,
    )
