from types import CoroutineType
from typing import Any, Callable

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models_schema.user.user import UserInput

# ----- REGISTER ----- #


@pytest.fixture(name="register_user_custom")
async def register_user_custom_fixture(
    client: AsyncClient,
    session: AsyncSession,
) -> Callable[[str], CoroutineType[Any, Any, None]]:
    """
    Returns a function that registers a user with a custom name.
    """

    async def register_user_custom(username: str) -> None:
        user = UserInput(
            username=f"{username}",
            email=f"{username}@gmail.com",
            password=f"{username}-password",
        )

        await client.post(
            "/api/user/register",
            json=user.model_dump(),
        )

        session.expire_all()

    return register_user_custom


@pytest.fixture(name="register_user_test")
async def register_user_test_fixture(
    register_user_custom: Callable[[str], CoroutineType[Any, Any, None]],
) -> None:
    """
    Automatically registers a user with the username "test".
    """

    await register_user_custom("test")


# ----- LOGIN ----- #


@pytest.fixture(name="login_user_custom")
async def login_user_custom_fixture(
    client: AsyncClient,
    register_user_custom: Callable[[str], CoroutineType[Any, Any, None]],
) -> Callable[[str], CoroutineType[Any, Any, None]]:
    """
    Returns a function that registers and logins a user with a custom name.
    """

    async def login_user_custom(username: str) -> None:
        await register_user_custom(username)

        response = await client.post(
            "/api/login",
            data={
                "username": "test@gmail.com",
                "password": "test-password",
            },
        )
        token = response.json().get("access_token")

        client.headers.update({"Authorization": f"Bearer {token}"})

    return login_user_custom


@pytest.fixture(name="login_user_test")
async def login_user_test_fixture(
    client: AsyncClient,
    register_user_test: None,
) -> None:
    """
    Automatically registers and logins a user with the username "test".
    """

    response = await client.post(
        "/api/login",
        data={
            "username": "test@gmail.com",
            "password": "test-password",
        },
    )
    token = response.json().get("access_token")

    client.headers.update({"Authorization": f"Bearer {token}"})
