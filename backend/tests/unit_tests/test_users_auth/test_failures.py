from types import CoroutineType
from typing import Any, Callable

import pytest
from httpx import AsyncClient
from pydantic import EmailStr

from backend.src.exceptions.core import ExceptionResponse, ExceptionType
from backend.src.models_schema.user.user import User, UserInput, UserPasswordChange
from backend.src.routes.user import UserUpdate
from backend.tests.utils.validators import (
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)

# ----- CREATE ----- #


@pytest.mark.parametrize(
    "username, email, password, status_code, exception_type",
    [
        (
            "",
            "test2@gmail.com",
            "test2-password",
            400,
            ExceptionType.REQUEST_VALIDATION,
        ),
        (
            "test2-username",
            "",
            "test2-password",
            400,
            ExceptionType.REQUEST_VALIDATION,
        ),
        (
            "test2-username",
            "test2@gmail.com",
            "",
            400,
            ExceptionType.REQUEST_VALIDATION,
        ),
        (
            "test2-username",
            "wrong-format",
            "test2-password",
            400,
            ExceptionType.REQUEST_VALIDATION,
        ),
        (
            "test-username",
            "test@gmail.com",
            "test-password",
            409,
            ExceptionType.TAKEN_INFO,
        ),
    ],
)
async def test_register_user(
    client: AsyncClient,
    register_user_test: User,
    username: str,
    email: str,
    password: str,
    status_code: int,
    exception_type: ExceptionType,
):
    """
    Fails to register a user with empty inputs, invalid email and overlapping email with another user.
    """
    response = await client.post(
        "/api/user/register",
        json={
            "username": username,
            "email": email,
            "description": "test-description",
            "password": password,
        },
    )

    validate_status_code(response, status_code)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(response, {"exception_type": exception_type})


# ----- AUTH ----- #


@pytest.mark.parametrize(
    "email, password",
    [
        ("wrong@gmail.com", "test-password"),
        ("test@gmail.com", "wrong-password"),
    ],
)
async def test_login_user(
    client: AsyncClient,
    register_user_test: User,
    email: EmailStr,
    password: str,
):
    """
    Fails to login with incorrect credentials.
    """
    response = await client.post(
        "/api/login",
        data={
            "username": email,
            "password": password,
        },
    )

    validate_status_code(response, 401)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.AUTHENTICATION}
    )


# ----- UPDATE ----- #


async def test_update_user(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    register_user_custom: Callable[[str], CoroutineType[Any, Any, None]],
):
    """
    Fails to update a user with overlapping email.
    """
    await register_user_custom("overlap")

    user_update = UserUpdate(
        email="overlap@gmail.com",
    )

    response = await client.patch(
        "/api/user/me",
        json=user_update.model_dump(exclude_unset=True),
    )

    validate_status_code(response, 409)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(response, {"exception_type": ExceptionType.TAKEN_INFO})


async def test_change_password(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
):
    """
    Fails to change password with incorrect incredentials.
    """
    user_password_change = UserPasswordChange(
        old_password="wrong-password", new_password="test-password-updated"
    )

    response = await client.patch(
        "/api/user/change-password",
        json=user_password_change.model_dump(),
    )

    validate_status_code(response, 401)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.WRONG_PASSWORD}
    )
