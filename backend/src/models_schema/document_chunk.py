from typing import TYPE_CHECKING, Annotated

from pgvector.sqlalchemy import Vector
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.src.models_schema.document import Document


class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunk"  # type: ignore

    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None
    document_id: Annotated[
        int | None, Field(foreign_key="document.id", nullable=False, ondelete="CASCADE")
    ] = None

    content_original: str
    content_embedded: Annotated[list[float], Field(sa_column=Column(Vector))]
    document_page_num: int | None = None  # What page current chunk is in
    document_chunk_index: int | None = None  # Chunk id in a document

    document: "Document" = Relationship(back_populates="document_chunks")
