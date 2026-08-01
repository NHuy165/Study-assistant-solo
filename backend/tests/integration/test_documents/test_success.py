from pathlib import Path

import pytest
from httpx import AsyncClient

from backend.src.core.config import settings
from backend.src.models_schema.document.document import DocumentOutput
from backend.src.models_schema.document.document_analysis import DocumentAnalysisOutput
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import DocumentType, SubjectType
from backend.src.models_schema.user.user import User
from backend.tests.utils.validators import (
    validate_response_contents,
    validate_response_model,
    validate_status_code,
)


@pytest.mark.skipif(
    not settings.RUN_INTEGRATION, reason="Auto skipping integration tests."
)
@pytest.mark.integration
@pytest.mark.parametrize(
    "filename, subject_type, document_type, MIME_type",
    [
        ("test_file_pdf.pdf", SubjectType.MATHS, DocumentType.PDF, "application/pdf"),
        ("test_file_txt.txt", SubjectType.LANGUAGES, DocumentType.TEXT, "text/plain"),
        (
            "test_file_image.webp",
            SubjectType.LITERATURE,
            DocumentType.IMAGE,
            "image/webp",
        ),
    ],
)
async def test_create_document(
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: Interaction,
    filename: str,
    subject_type: SubjectType,
    document_type: DocumentType,
    MIME_type: str,
):
    """
    Tests all API calls in a document uploading process.
    """

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

    validate_status_code(response, 200)
    validate_response_model(response, tuple[DocumentOutput, DocumentAnalysisOutput])
    validate_response_contents(
        response,
        [
            {
                "name": filename,
                "subject_type": subject_type,
                "type": document_type.value,
            },
        ],
    )
