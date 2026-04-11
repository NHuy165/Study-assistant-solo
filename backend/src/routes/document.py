from typing import Annotated

from fastapi import APIRouter, Body, Form, Query, UploadFile, status

from backend.src.core.database import SessionDep
from backend.src.core.dependencies import InteractionDep, UserDep
from backend.src.exceptions.core import Responses
from backend.src.models_schema.document import (
    DocumentInput,
    DocumentOutput,
    DocumentUpdate,
)
from backend.src.services import document, document_chunk

router = APIRouter()


# ----- CREATE ----- #


@router.post(
    "/{interaction_id}/upload",
    response_model=DocumentOutput,
    responses={
        400: Responses.RESPONSE_400_BAD_REQUEST,
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def save_document(
    user: UserDep,
    session: SessionDep,
    file: UploadFile,
    document_input: Annotated[DocumentInput, Query()],
    interaction: InteractionDep,
):
    """
    Embeds and saves a user-uploaded document to the database. Documents belong to an interaction.
    """
    document_output = await document.save_document(
        session, file, interaction, document_input
    )

    await session.refresh(document_output)

    return document_output


# ----- READ ----- #


@router.get(
    "/{interaction_id}/",
    response_model=list[DocumentOutput],
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def read_all_documents(
    user: UserDep,
    session: SessionDep,
    interaction: InteractionDep,
):
    """
    Reads all documents in an interaction.
    """
    documents_output = await document.read_all_documents(session, interaction)
    return documents_output


# ----- UPDATE ----- #


@router.patch(
    "/{document_id}",
    response_model=DocumentOutput,
    responses={
        400: Responses.RESPONSE_400_BAD_REQUEST,
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def update_document(
    user: UserDep,
    session: SessionDep,
    document_id: int,
    document_update: DocumentUpdate,
):
    """
    Updates a document's information. Document's contents cannot be updated.
    """
    document_output = await document.update_document(
        user, session, document_id, document_update
    )
    return document_output


# ----- DELETE ----- #


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: Responses.RESPONSE_401_UNAUTHORIZED,
        404: Responses.RESPONSE_404_NOT_FOUND,
    },
)
async def delete_document(
    user: UserDep,
    session: SessionDep,
    document_id: int,
):
    """
    Deletes a document from an interaction.
    """
    await document.delete_document(user, session, document_id)
