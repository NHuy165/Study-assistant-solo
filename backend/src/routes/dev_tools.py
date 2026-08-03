from typing import Annotated

from fastapi import APIRouter, Query, UploadFile

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
from backend.src.models_schema.document.document import DocumentInput, DocumentOutput
from backend.src.models_schema.document.document_analysis import DocumentAnalysisOutput
from backend.src.models_schema.llm_response.llm_response import (
    LLMResponseInput,
    LLMResponseOutput,
)
from backend.src.models_schema.study_progress.assessment import (
    MockStudyAssessmentInput,
    StudyAssessmentOutput,
)
from backend.src.services.dev_tools import (
    document,
    llm_response,
    study_activity,
    study_assessment,
)

router = APIRouter()


@router.post("/wipe-db", status_code=204)
async def wipe_database():
    await reset_database()


@router.get("/ping", status_code=204)
async def ping(session: SessionDep):
    await session.execute(select(1))


@router.post(
    "/document/{interaction_id}",
    tags=["document"],
    response_model=tuple[DocumentOutput, DocumentAnalysisOutput | None],
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def mock_save_document(
    user: UserDep,
    session: SessionDep,
    current_datetime: DatetimeDep,
    file: UploadFile,
    document_input: Annotated[DocumentInput, Query()],
    interaction: InteractionDep,
):
    """
    Mock saves a user-uploaded document to the database, no embedding takes place.
    """
    document_output, document_analysis = await document.mock_save_document(
        user=user,
        session=session,
        current_datetime=current_datetime,
        file=file,
        interaction=interaction,
        document_input=document_input,
    )

    return document_output, document_analysis


@router.post(
    "/llm-response/{interaction_id}",
    tags=["llm-response"],
    response_model=LLMResponseOutput,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def mock_create_llm_response(
    user: UserDep,
    session: SessionDep,
    current_datetime: DatetimeDep,
    interaction: InteractionDep,
    llm_response_input: LLMResponseInput,
):
    """
    Receives a user prompt and mocks a model's answer.
    """
    llm_response_output = await llm_response.mock_create_llm_response(
        user=user,
        session=session,
        current_datetime=current_datetime,
        llm_response_input=llm_response_input,
        interaction=interaction,
    )

    return llm_response_output


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
    Mocks a study activity with predictable contents.
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
    Mock submits an existing exercise activity with predictable contents.
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


@router.post(
    "/study-assessment",
    tags=["study-progress"],
    response_model=StudyAssessmentOutput,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def mock_create_study_assessment(
    user: UserDep,
    session: SessionDep,
    current_datetime: DatetimeDep,
    mock_study_assessment_input: MockStudyAssessmentInput,
):
    """
    Mocks a study assessment with predictable contents.
    """
    result = await study_assessment.mock_create_study_assessment(
        user=user,
        session=session,
        current_datetime=current_datetime,
        mock_study_assessment_input=mock_study_assessment_input,
    )

    return result
