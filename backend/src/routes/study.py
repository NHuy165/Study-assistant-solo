from fastapi import APIRouter, status

from backend.src.core.database import SessionDep
from backend.src.core.dependencies import UserDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.study import ModelPrompt, ModelResponse
from backend.src.services.study import core as study

router = APIRouter()

# ----- CREATE ----- #


@router.post(
    "/sources/{file_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def save_chunks(user: UserDep, session: SessionDep, file_name: str):
    await study.save_chunks(session, file_name)


# ----- READ ----- #


@router.post(
    "/ask",
    response_model=ModelResponse,
    responses={
        400: Responses.RESPONSE_400_BAD_REQUEST,
    },
)
async def answer_query(user: UserDep, session: SessionDep, prompt: ModelPrompt):
    result = await study.answer_query(session, prompt)
    return result
