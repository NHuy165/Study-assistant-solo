from fastapi import APIRouter

from backend.src.core.database import SessionDep
from backend.src.route_services.study import answer_query_service, save_chunks_service

router = APIRouter()


@router.post("/sources/{file_name}")
async def save_chunks(session: SessionDep, file_name: str):
    await save_chunks_service(session, file_name)


@router.get("/ask")
async def answer_query(session: SessionDep, query: str):
    result = await answer_query_service(session, query)
    return {"answer": result}
