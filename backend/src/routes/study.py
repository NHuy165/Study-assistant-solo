from fastapi import APIRouter, status

from backend.src.core.database import SessionDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.study import ModelPrompt, ModelResponse
from backend.src.services.study.core import answer_query_service, save_chunks_service

router = APIRouter()

# ----- CREATE ----- #


@router.post(
    "/sources/{file_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def save_chunks(session: SessionDep, file_name: str):
    await save_chunks_service(session, file_name)


# ----- READ ----- #


@router.post(
    "/ask",
    response_model=ModelResponse,
    responses={
        400: Responses.RESPONSE_400_BAD_REQUEST,
    },
)
async def answer_query(session: SessionDep, prompt: ModelPrompt):
    result = await answer_query_service(session, prompt)
    return result
