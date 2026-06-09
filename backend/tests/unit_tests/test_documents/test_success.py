from pathlib import Path
from unittest.mock import patch

from fastapi.background import P
from httpx import AsyncClient

from backend.src.core.ai_api import GlobalAPI
from backend.src.core.config import settings
from backend.src.models_schema.document.document import DocumentOutput
from backend.src.models_schema.document.document_analysis import (
    DocumentAnalysisOutput,
    DocumentAnalysisSchema,
    MaterialRecommendationSchema,
    QuestionRecommendationSchema,
)
from backend.src.models_schema.miscellaneous.enums import (
    StudyActivityFormat,
    SubjectType,
)
from backend.src.models_schema.user.user import User
from backend.tests.utils.validators import (
    validate_model,
    validate_response_contents,
    validate_status_code,
)


@patch.object(GlobalAPI, "generate_document_analysis")
@patch.object(GlobalAPI, "mass_embed")
async def test_create_document(
    mock_GlobalAPI_mass_embed,
    mock_GlobalAPI_generate_document_analysis,
    client: AsyncClient,
    register_user_test: User,
    login_user_test: None,
    create_interaction_test: int,
) -> None:
    """
    Uploads a document.
    """

    # Mock embedding
    mock_GlobalAPI_mass_embed.return_value = [
        [0.1] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE,
        [0.2] * settings.DEFAULT_EMBED_DIMENSIONALITY_CLOUDFLARE,
    ]

    # Mock document analysis
    mock_summary = "Mock document analysis."
    mock_material = MaterialRecommendationSchema(
        prompt="Mock material generation prompt.",
        activity_format=StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
        subject_type=SubjectType.MATHS,
    )
    mock_question = QuestionRecommendationSchema(prompt="Mock question prompt.")
    mock_analysis = DocumentAnalysisSchema(
        summary=mock_summary,
        subject_type=SubjectType.MATHS,
        subject_type_overwrite=True,
        material_recommendations=[mock_material],
        question_recommendations=[mock_question],
    )
    mock_GlobalAPI_generate_document_analysis.return_value = (
        mock_analysis.model_dump_json()
    )

    filepath = (
        Path(__file__).resolve().parent.parent.parent / "test_data" / "test_file.pdf"
    )

    with open(filepath, "rb") as f:
        response = await client.post(
            f"/api/document/{create_interaction_test}/upload",
            files={"file": ("test_file.pdf", f, "application/pdf")},
        )

    validate_status_code(response, 200)
    validate_model(response, tuple[DocumentOutput, DocumentAnalysisOutput])
    validate_response_contents(
        response,
        [
            {
                "name": "test_file.pdf",
                "subject_type": SubjectType.MATHS,
                "type": "PDF",
            },
            mock_analysis.model_dump(
                exclude={"subject_type", "subject_type_overwrite"}
            ),
        ],
    )
