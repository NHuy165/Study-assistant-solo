from fastapi import APIRouter

from backend.src.core.dependencies import SessionDep, UserDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.miscellaneous.enums import AggregateTarget
from backend.src.models_schema.study_progress import Criterion
from backend.src.services import study_progress

router = APIRouter()


@router.post(
    "/",
    response_model=list[tuple],
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def get_study_progress(
    user: UserDep,
    session: SessionDep,
    criteria: list[Criterion],
    target: AggregateTarget,
):
    result = await study_progress.get_study_progress(
        user,
        session,
        criteria,
        target,
    )

    return result
