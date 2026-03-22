from fastapi import APIRouter

from backend.src.core.database import SessionDep
from backend.src.models_schema.users import UserInput, UserOutput
from backend.src.services import users

router = APIRouter()

# ----- CREATE ----- #


@router.post("/register", response_model=UserOutput)
async def register_user(session: SessionDep, user_input: UserInput):
    user = await users.register_user(session, user_input)
    return user
