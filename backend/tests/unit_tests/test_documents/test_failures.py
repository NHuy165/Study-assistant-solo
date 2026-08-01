from pathlib import Path
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
from backend.src.models_schema.document.document_analysis import (
    DocumentAnalysisSchema,
)
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.user.user import User
from backend.tests.fixtures.documents import SubjectType
from backend.tests.utils.validators import (
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)


@pytest.mark.parametrize(
    "filename, query_parameters",
    [
        ("test_file_pdf.pdf", ""),
        ("test_file_pdf.pdf", "?subject_type=MATHS&subject_type_overwrite=true"),
        ("test_file_wrong.xlsx", "?subject_type_overwrite=false"),
    ],
)
async def test_create_document(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    filename: str,
    query_parameters: str,
) -> None:
    """
    Fails to upload a document by not specifying overwrite mode.
    Fails to upload a document by setting overwrite to true while subject type is not null.
    Fails to upload a document with invalid format.
    """

    filepath = (
        Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "documents"
        / filename
    )

    with open(filepath, "rb") as f:
        response = await client.post(
            f"/api/document/{create_interaction_test.id}{query_parameters}",
            files={"file": ("test_file.pdf", f, "application/pdf")},
        )

        validate_status_code(response, 400)
        validate_response_model(response, ExceptionResponse)
        validate_response_contents(
            response, {"exception_type": ExceptionType.REQUEST_VALIDATION}
        )


@pytest.mark.parametrize(
    "endpoint_failure, filename, MIME_type",
    [
        ("generate_document_analysis", "test_file_pdf.pdf", "application/pdf"),
        ("mass_embed", "test_file_txt.txt", "text/plain"),
        ("caption_image", "test_file_image.webp", "image/webp"),
    ],
)
@patch.object(GlobalAPI, "generate_document_analysis")
@patch.object(GlobalAPI, "mass_embed")
@patch.object(GlobalAPI, "caption_image")
async def test_create_document_failed_api(
    mock_GlobalAPI_caption_image: AsyncMock,
    mock_GlobalAPI_mass_embed: AsyncMock,
    mock_GlobalAPI_generate_document_analysis: AsyncMock,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    endpoint_failure: str,
    filename: str,
    MIME_type: str,
) -> None:
    """
    Fails to upload a document due to unavailable external API service.
    """

    # Mock embedding
    if endpoint_failure == "mass_embed":
        mock_GlobalAPI_mass_embed.side_effect = ExceptionExternalService_503(
            "API failure."
        )
    else:
        mock_GlobalAPI_mass_embed.return_value = [
            [0.1] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE,
        ]

    # Mock document analysis
    if endpoint_failure == "generate_document_analysis":
        mock_GlobalAPI_generate_document_analysis.side_effect = (
            ExceptionExternalService_503("API failure.")
        )
    else:
        mock_summary = "Mock document analysis."
        mock_analysis = DocumentAnalysisSchema(
            summary=mock_summary,
            subject_type=SubjectType.MATHS,
            material_recommendations=[],
            question_recommendations=[],
        )
        mock_GlobalAPI_generate_document_analysis.return_value = (
            mock_analysis.model_dump_json()
        )

    # Mock image captaining
    if endpoint_failure == "caption_image":
        mock_GlobalAPI_caption_image.side_effect = ExceptionExternalService_503(
            "API failure."
        )
    else:
        mock_GlobalAPI_caption_image.return_value = "Mock image captioning"

    filepath = (
        Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "documents"
        / filename
    )

    with open(filepath, "rb") as f:
        response = await client.post(
            f"/api/document/{create_interaction_test.id}?subject_type_overwrite=true",
            files={"file": (filename, f, MIME_type)},
        )

    validate_status_code(response, 503)
    validate_response_model(response, ExceptionResponse)
    validate_response_contents(
        response, {"exception_type": ExceptionType.EXTERNAL_SERVICE}
    )
