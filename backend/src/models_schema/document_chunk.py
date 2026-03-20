from typing import Annotated

from pgvector.sqlalchemy import Vector
from sqlmodel import Column, Field, SQLModel


class DocumentChunk(SQLModel, table=True):
    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None

    content_original: str
    content_embedded: Annotated[list[float], Field(sa_column=Column(Vector))]

    document_name: str
    document_page_num: int
    document_chunk_index: int
    # Implement user_id later
