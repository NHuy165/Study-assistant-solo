from datetime import date
from typing import Annotated

from fastapi import APIRouter
from sqlmodel import Field

from backend.src.core.dependencies import DayOverwriteDep, SessionDep, UserDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.miscellaneous.enums import AggregateTarget
from backend.src.models_schema.study_progress.assessment import StudyAssessmentOutput
from backend.src.models_schema.study_progress.criterion import Criterion
from backend.src.services import study_progress

router = APIRouter()

# ----- CREATE ----- #


@router.post(
    "/study-assessment",
    response_model=StudyAssessmentOutput | None,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def create_study_assessment(
    user: UserDep,
    session: SessionDep,
    day_overwrite: DayOverwriteDep,
):
    result = await study_progress.create_study_assessment(
        user,
        session,
        day_overwrite,
    )

    return result


# ----- READ ----- #


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
    result = await study_progress.read_latest_study_assessment(
        user,
        session,
    )

    return result

@router.get(
    "/study-assessment",
    response_model=StudyAssessmentOutput,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND
    },
)
async def read_study_assessment_by_date(
    user: UserDep,
    session: SessionDep,
    specific_date: date
):
    result = await study_progress.read_study_assessment_by_date(
        user,
        session,
        specific_date,
    )

    return result

@router.get(
    "/study-assessment",
    response_model=StudyAssessmentOutput,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def read_study_assessment_by_date(
    user: UserDep, session: SessionDep, specific_date: date
):
    result = await study_progress.read_study_assessment_by_date(
        user,
        session,
        specific_date,
    )

    return result


@router.get(
    "/study-assessment/",
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
    result = await study_progress.read_study_assessments(
        user,
        session,
        offset,
        limit,
    )

    return result
