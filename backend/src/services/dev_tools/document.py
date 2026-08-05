from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import col, delete, select

from backend.src.exceptions.core import (
    ExceptionNotFound_404,
    ExceptionRequest_400,
    ExceptionRequestValidation_400,
)
from backend.src.models_schema.document.document import (
    Document,
    DocumentInput,
    DocumentUpdate,
)
from backend.src.models_schema.document.document_analysis import (
    DocumentAnalysis,
    MaterialRecommendation,
    QuestionRecommendation,
)
from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.miscellaneous.enums import (
    DocumentType,
    StudyActivityFormat,
    SubjectType,
)
from backend.src.models_schema.user.user import User
from backend.src.RAG.chunking.base import DocumentExtractor
from backend.src.RAG.chunking.image import ImageExtractor
from backend.src.RAG.chunking.PDF import PdfExtractor
from backend.src.RAG.chunking.text import TextExtractor


async def mock_save_document(
    user: User,
    session: AsyncSession,
    current_datetime: datetime,
    file: UploadFile,
    interaction: Interaction,
    document_input: DocumentInput,
) -> tuple[Document, DocumentAnalysis | None]:

    # Verifies document type and picks extractor
    EXTRACTORS: dict[DocumentType, type[DocumentExtractor]] = {
        DocumentType.PDF: PdfExtractor,
        DocumentType.IMAGE: ImageExtractor,
        DocumentType.TEXT: TextExtractor,
    }

    selected_type = None
    selected_extractor = None

    for doc_type, extractor in EXTRACTORS.items():
        if extractor.verify(file):
            selected_type = doc_type
            selected_extractor = extractor
            break

    if selected_type is None or selected_extractor is None:
        raise ExceptionRequestValidation_400(
            "Invalid file format.\nAllowed formats are:\n- PDF\n- JPEG, PNGM, WEBP\n- Text files\nPlease recheck file extension and file contents."
        )

    # Name check
    if document_input.name is None:
        name = file.filename if file.filename else ""
    else:
        name = document_input.name

    if not name:
        raise ExceptionRequest_400(
            "Document name cannot be blank. Either specify a name to be overwritten or change the document's original name."
        )

    # Page start check
    page_starts_at = document_input.page_starts_at
    if selected_type not in (DocumentType.PDF):
        page_starts_at = 0

    # Saves document
    document = Document(
        name=name,
        interaction=interaction,
        page_starts_at=page_starts_at,
        type=selected_type,
        subject_type=document_input.subject_type
        if document_input.subject_type
        else SubjectType.OTHER,  # Temporary
        text=f"Document {name} contents",
        created_at=current_datetime,
    )

    if document_input.subject_type_overwrite:
        document.subject_type = SubjectType.MATHS  # Hard coded

    # Mocks document analysis
    material_recommendations = [
        MaterialRecommendation(
            prompt=f"Study activity prompt of document {name}",
            activity_format=StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS,
            subject_type=document_input.subject_type
            if document_input.subject_type is not None
            else SubjectType.MATHS,
        ),
    ]
    question_recommendations = [
        QuestionRecommendation(prompt=f"Chat prompt of document {name}")
    ]
    document_analysis = DocumentAnalysis(
        summary=f"Summary of {name}",
        material_recommendations=material_recommendations,
        question_recommendations=question_recommendations,
    )

    document.document_analysis = document_analysis

    session.add(document)
    await session.commit()

    return document, document_analysis
