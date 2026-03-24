from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.src.exceptions.core import ExceptionNotFound_404, ExceptionRequest_400
from backend.src.models_schema.document import Document, DocumentUpdate
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.user import User

# ----- CREATE ----- #


def verify_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise ExceptionRequest_400("Invalid PDF file.")

    header = file.file.read(5)
    file.file.seek(0)

    if header != b"%PDF-":
        raise ExceptionRequest_400("Invalid PDF file.")


async def save_document(
    session: AsyncSession, file: UploadFile, interaction: Interaction
) -> Document:
    verify_pdf(file)

    assert file.filename is not None

    document = Document(name=file.filename, interaction=interaction)

    session.add(document)
    await session.commit()
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
