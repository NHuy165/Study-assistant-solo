from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.core.database import SessionDep
from backend.src.models_schema.auth import Token
from backend.src.services import auth

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_token(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    token = await auth.login_for_token(session, user.username, user.password)
    return token
