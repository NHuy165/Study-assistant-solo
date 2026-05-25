from fastapi import APIRouter

from backend.src.core.database import reset_database

router = APIRouter()


@router.post("/wipe-db", status_code=204)
async def wipe_database():
    await reset_database()
