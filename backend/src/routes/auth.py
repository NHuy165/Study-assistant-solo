from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.core.database import SessionDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.auth import Token
from backend.src.services import auth

router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
    },
)
async def login_for_token(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    """
    Login endpoint. Returns a token when user enters correct credentials. Tokens have an expiration time.
    """
    token = await auth.login_for_token(session, user.username, user.password)
    return token
