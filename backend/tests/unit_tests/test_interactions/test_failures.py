from httpx import AsyncClient

from backend.src.exceptions.core import ExceptionResponse, ExceptionType
from backend.src.models_schema.interaction.interaction import (
    InteractionInput,
)
from backend.src.models_schema.user.user import User
from backend.tests.utils.validators import (
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)


async def test_create_interaction(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
) -> None:
    """
    Fails to create an interaction with an empty name.
    """
    response = await client.post(
        "/api/interaction", json={"name": "", "description": "test-description"}
    )

    validate_status_code(response, 400)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.REQUEST_VALIDATION}
    )
