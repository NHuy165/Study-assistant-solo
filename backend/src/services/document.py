from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.src.exceptions.core import ExceptionNotFound_404, ExceptionRequest_400
from backend.src.models_schema.document import Document, DocumentInput, DocumentUpdate
from backend.src.models_schema.enums import DocumentType
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.user import User
from backend.src.services import document_chunk

# ----- CREATE ----- #


def verify_pdf(file: UploadFile):
    """
    Verifies if the file is a PDF.
    """

    # === Content type === #
    if file.content_type != "application/pdf":
        return False

    # === Header === #
    header = file.file.read(5)
    file.file.seek(0)

    if header != b"%PDF-":
        return False

    return True


def verify_image(file: UploadFile) -> bool:
    """
    Verifies if the file is an image.
    """

    # === Content type === #
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        return False

    # === Header === #
    header = file.file.read(12)
    file.file.seek(0)

    is_jpeg = header.startswith(b"\xff\xd8\xff")
    is_png = header.startswith(b"\x89PNG\r\n\x1a\n")
    is_webp = header.startswith(b"RIFF") and header[8:12] == b"WEBP"

    if not (is_jpeg or is_png or is_webp):
        return False

    return True


def verify_text(file: UploadFile):
    """
    Verifies if the file is a text file.
    """

    # === Content type === #
    if file.content_type is None:
        return False

    is_text = (
        file.content_type.startswith("text/") or file.content_type == "application/json"
    )
    is_generic = file.content_type == "application/octet-stream"

    if not (is_text or is_generic):
        return False

    # === Header === #
    header = file.file.read(512)
    file.file.seek(0)

    if not header:
        return False

    try:
        header.decode("utf-8")
        return True

    except UnicodeDecodeError:
        return False


def file_format_checker(
    file: UploadFile, input_offset: int
) -> tuple[DocumentType, int]:
    if verify_pdf(file):
        document_type = DocumentType.PDF
        page_starts_at = input_offset
    elif verify_image(file):
        document_type = DocumentType.IMAGE
        page_starts_at = 0
    elif verify_text(file):
        document_type = DocumentType.TEXT
        page_starts_at = 0
    else:
        raise ExceptionRequest_400(
            "Invalid file format.\nAllowed formats are:\n- PDF\n- JPEG, PNGM, WEBP\n- Text files\nPlease recheck file extension and file contents."
        )
    return document_type, page_starts_at


async def file_saver(
    session: AsyncSession, file: UploadFile, document: Document
) -> None:
    if document.type == DocumentType.PDF:
        await document_chunk.save_pdf_chunks(
            session,
            file,
            document,
        )
    elif document.type == DocumentType.IMAGE:
        await document_chunk.save_image_chunks(
            session,
            file,
            document,
        )
    elif document.type == DocumentType.TEXT:
        await document_chunk.save_text_chunks(
            session,
            file,
            document,
        )


async def save_document(
    session: AsyncSession,
    file: UploadFile,
    interaction: Interaction,
    document_input: DocumentInput,
) -> Document:

    document_type, page_starts_at = file_format_checker(
        file, document_input.page_starts_at
    )

    if document_input.name is None:
        name = file.filename if file.filename else ""
    else:
        name = document_input.name

    # Saves document
    document = Document(
        name=name,
        interaction=interaction,
        page_starts_at=page_starts_at,
        type=document_type,
    )

    session.add(document)
    await session.commit()
    await session.refresh(document)

    # Saves document contents
    await file_saver(session, file, document)

    await session.refresh(document)

    return document


# ----- READ ----- #


async def read_all_documents(
    session: AsyncSession, interaction: Interaction
) -> list[Document]:
    query = select(Document).where(Document.interaction_id == interaction.id)
    documents = (await session.execute(query)).scalars().all()

    return list(documents)


# ----- UPDATE ----- #


async def update_document(
    user: User,
    session: AsyncSession,
    document_id: int,
    document_update: DocumentUpdate,
) -> Document:

    query = (
        select(Document)
        .join(Interaction)
        .where(
            Document.id == document_id,
            Interaction.user_id == user.id,
        )
    )
    document = (await session.execute(query)).scalars().first()

    if document is None:
        raise ExceptionNotFound_404(
            "Document",
            {
                "id": document_id,
                "interaction.user_id": user.id,
            },
        )

    # Update logic
    update_data = document_update.model_dump(exclude_unset=True)

    if document.type == DocumentType.IMAGE:
        update_data["page_starts_at"] = 0

    document.sqlmodel_update(update_data)

    await session.commit()
    await session.refresh(document)

    return document


# ----- DELETE ----- #


async def delete_document(
    user: User,
    session: AsyncSession,
    document_id: int,
) -> None:
    query = (
        select(Document)
        .join(Interaction)
        .where(
            Document.id == document_id,
            Interaction.user_id == user.id,
        )
    )
    document = (await session.execute(query)).scalars().first()

    if document is None:
        raise ExceptionNotFound_404(
            "Document",
            {
                "id": document_id,
                "interaction.user_id": user.id,
            },
        )

    await session.delete(document)
    await session.commit()
