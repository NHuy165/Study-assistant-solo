from fastapi import APIRouter

from backend.src.core.database import SessionDep
from backend.src.models_schema.study import ModelPrompt
from backend.src.services.study.core import answer_query_service, save_chunks_service

router = APIRouter()

# ----- CREATE ----- #


@router.post("/sources/{file_name}")
async def save_chunks(session: SessionDep, file_name: str):
    await save_chunks_service(session, file_name)


# ----- READ ----- #


@router.post("/ask")
async def answer_query(session: SessionDep, prompt: ModelPrompt):
    result = await answer_query_service(session, prompt)
    return {"answer": result}
