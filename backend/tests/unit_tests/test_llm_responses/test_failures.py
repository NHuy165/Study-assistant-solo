from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from backend.src.core.ai_api import GlobalAPI
from backend.src.core.config import settings
from backend.src.exceptions.core import (
    ExceptionExternalService_503,
    ExceptionResponse,
    ExceptionType,
)
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.user.user import User
from backend.tests.utils.validators import (
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)


@patch.object(GlobalAPI, "generate_chat")
@patch.object(GlobalAPI, "embed")
@patch.object(GlobalAPI, "rewrite_prompt")
@pytest.mark.parametrize(
    "endpoint_failure",
    [
        ("generate_chat"),
        ("embed"),
        ("rewrite_prompt"),
    ],
)
async def test_create_llm_response_failed_api(
    mock_GlobalAPI_rewrite_prompt: AsyncMock,
    mock_GlobalAPI_embed: AsyncMock,
    mock_GlobalAPI_generate_chat: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    endpoint_failure: str,
):
    """
    Fails to chat with the LLM due to unavailable external API service.
    """

    # Mock prompt rewrite
    if endpoint_failure == "rewrite_prompt":
        mock_GlobalAPI_rewrite_prompt.side_effect = ExceptionExternalService_503(
            "API failure.",
        )
    else:
        mock_GlobalAPI_rewrite_prompt.return_value = "Mock rewritten prompt"

    # Mock embedding
    if endpoint_failure == "embed":
        mock_GlobalAPI_embed.side_effect = ExceptionExternalService_503(
            "API failure.",
        )
    else:
        mock_GlobalAPI_embed.return_value = [
            0.1
        ] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE

    # Mock chat generation
    if endpoint_failure == "generate_chat":
        mock_GlobalAPI_generate_chat.side_effect = ExceptionExternalService_503(
            "API failure.",
        )
    else:
        mock_GlobalAPI_generate_chat.return_value = "Mock LLM response."

    response = await client.post(
        f"/api/llm-response/{create_interaction_test.id}",
        json={"prompt": "LLM call prompt."},
    )
    validate_status_code(response, 503)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.EXTERNAL_SERVICE}
    )
