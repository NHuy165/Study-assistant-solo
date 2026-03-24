from datetime import datetime, timezone
from typing import TYPE_CHECKING, Annotated

from fastapi import UploadFile
from pydantic import BeforeValidator
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from backend.src.models_schema.utils import beva_forbid_none

if TYPE_CHECKING:
    from backend.src.models_schema.document_chunk import DocumentChunk
    from backend.src.models_schema.interaction import Interaction

# ----- BASE ----- #


class DocumentBase(SQLModel):
    name: str


# ----- INPUT ----- #


# ----- OUTPUT ----- #


class DocumentOutput(DocumentBase):
    id: int
    created_at: datetime


# ----- UPDATE ----- #


class DocumentUpdate(SQLModel):
    name: Annotated[str, Field(min_length=1)]


# ----- TABLE MODEL ----- #


class Document(DocumentBase, table=True):
    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None
    interaction_id: Annotated[
        int | None,
        Field(foreign_key="interaction.id", nullable=False, ondelete="CASCADE"),
    ] = None

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    interaction: "Interaction" = Relationship(back_populates="documents")
    document_chunks: list["DocumentChunk"] = Relationship(
        back_populates="document", cascade_delete=True
    )
