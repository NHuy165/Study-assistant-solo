from fastapi import APIRouter

from backend.src.core.database import SessionDep
from backend.src.models_schema.user import UserInput, UserOutput
from backend.src.services import user

router = APIRouter()

# ----- CREATE ----- #


@router.post("/register", response_model=UserOutput)
async def register_user(session: SessionDep, user_input: UserInput):
    """
    Creates a user account.
    """
    user_output = await user.register_user(session, user_input)
    return user_output
