from datetime import date
from typing import Annotated

from fastapi import APIRouter
from sqlmodel import Field

from backend.src.core.dependencies import DatetimeDep, SessionDep, UserDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.miscellaneous.enums import AggregateTarget
from backend.src.models_schema.study_progress.assessment import StudyAssessmentOutput
from backend.src.models_schema.study_progress.criterion import Criterion
from backend.src.services import study_progress

router = APIRouter()

# ----- CREATE ----- #


@router.post(
    "/study-assessment",
    response_model=list[StudyAssessmentOutput],
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def create_study_assessment(
    user: UserDep,
    session: SessionDep,
    current_datetime: DatetimeDep,
):
    """
    Creates a daily study assessment for every past daily check in without a study assessment (multiple ones may pile up if user goes straight to a function instead of going to the Home page first).
    """
    result = await study_progress.create_study_assessment(
        user=user,
        session=session,
        current_datetime=current_datetime,
    )

    return result


# ----- READ ----- #


@router.post(
    "",
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
    """
    Fetches user study statistics based on input parameters.
    """
    result = await study_progress.get_study_progress(
        user=user,
        session=session,
        criteria=criteria,
        target=target,
    )

    return result


@router.get(
    "/study-assessment/latest",
    response_model=StudyAssessmentOutput | None,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def read_latest_study_assessment(
    user: UserDep,
    session: SessionDep,
):
    """
    Reads the latest study assessment.
    """
    result = await study_progress.read_latest_study_assessment(
        user=user,
        session=session,
    )

    return result


@router.get(
    "/study-assessment/by-date",
    response_model=StudyAssessmentOutput,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def read_study_assessment_by_date(
    user: UserDep, session: SessionDep, specific_date: date
):
    """
    Reads a study assessment by date.
    """
    result = await study_progress.read_study_assessment_by_date(
        user=user,
        session=session,
        specific_date=specific_date,
    )

    return result


@router.get(
    "/study-assessment",
    response_model=list[StudyAssessmentOutput],
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def read_study_assessments(
    user: UserDep,
    session: SessionDep,
    offset: Annotated[int | None, Field(ge=0)] = None,
    limit: Annotated[int | None, Field(ge=0)] = None,
):
    """
    Reads all study assessments, supports 'offset' and 'limit' parameters.
    """
    result = await study_progress.read_study_assessments(
        user,
        session,
        offset,
        limit,
    )

    return result
