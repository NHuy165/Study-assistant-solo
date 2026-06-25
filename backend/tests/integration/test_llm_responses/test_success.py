import pytest
from httpx import AsyncClient

from backend.src.core.config import settings
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.llm_response.llm_response import (
    LLMResponseInput,
    LLMResponseOutput,
)
from backend.src.models_schema.user.user import User
from backend.tests.utils.validators import (
    validate_response_model,
    validate_status_code,
)


@pytest.mark.skipif(
    not settings.RUN_INTEGRATION, reason="Auto skipping integration tests."
)
@pytest.mark.integration
async def test_create_llm_response(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
):
    """
    Tests all API calls in an LLM chatting process.
    """

    llm_response_input = LLMResponseInput(prompt="What are fractions.")

    response = await client.post(
        f"/api/llm-response/{create_interaction_test.id}",
        json=llm_response_input.model_dump(),
    )

    validate_status_code(response, 200)
    validate_response_model(response, LLMResponseOutput)
