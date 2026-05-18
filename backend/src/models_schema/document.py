from datetime import datetime, timezone
from typing import TYPE_CHECKING, Annotated

from pydantic import BeforeValidator
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from backend.src.models_schema.miscellaneous.enums import DocumentType
from backend.src.models_schema.miscellaneous.utils import beva_forbid_none

if TYPE_CHECKING:
    from backend.src.models_schema.document_chunk import DocumentChunk
    from backend.src.models_schema.interaction import Interaction

# ----- BASE ----- #


class DocumentBase(SQLModel):
    name: str
    page_starts_at: int = 1


# ----- INPUT ----- #


class DocumentInput(DocumentBase):
    name: Annotated[str | None, BeforeValidator(beva_forbid_none)] = None


# ----- OUTPUT ----- #


class DocumentOutput(DocumentBase):
    id: int
    created_at: datetime
    type: DocumentType


# ----- UPDATE ----- #


class DocumentUpdate(DocumentBase):
    name: Annotated[str | None, BeforeValidator(beva_forbid_none)] = None
    page_starts_at: Annotated[int | None, BeforeValidator(beva_forbid_none)] = None


# ----- TABLE MODEL ----- #


class Document(DocumentBase, table=True):
    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None
    interaction_id: Annotated[
        int | None,
        Field(foreign_key="interaction.id", nullable=False, ondelete="CASCADE"),
    ] = None

    created_at: Annotated[
        datetime,
        Field(
            sa_column=Column(DateTime(timezone=True)),
            default_factory=lambda: datetime.now(timezone.utc),
        ),
    ]
    type: DocumentType

    interaction: "Interaction" = Relationship(back_populates="documents")
    document_chunks: list["DocumentChunk"] = Relationship(
        back_populates="document", cascade_delete=True
    )
