from typing import Iterable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import and_, col, or_, select

from backend.src.core.config import settings
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.interaction import Interaction


def RRF(
    vector_chunks: Sequence[DocumentChunk],
    keyword_chunks: Sequence[DocumentChunk],
) -> list[DocumentChunk]:
    """
    Selects a few best chunks from the vector search and keyword search chunks.
    """
    fused_scores: dict[int, float] = {}
    chunk_map: dict[int, DocumentChunk] = {}
    k = 60

    # Score vector chunks
    for rank, chunk in enumerate(vector_chunks):
        assert chunk.id is not None
        chunk_map[chunk.id] = chunk
        fused_scores[chunk.id] = 1.0 / (rank + 1 + k)

    # Score keyword chunks
    for rank, chunk in enumerate(keyword_chunks):
        assert chunk.id is not None
        if chunk.id not in chunk_map:
            chunk_map[chunk.id] = chunk
            fused_scores[chunk.id] = 0.0
        fused_scores[chunk.id] += 1.0 / (rank + 1 + k)

    sorted_chunk_ids = sorted(fused_scores, key=lambda k: fused_scores[k], reverse=True)
    top_chunk_ids = sorted_chunk_ids[: settings.N_CHUNKS_RETRIEVED]

    core_chunks = [chunk_map[i] for i in top_chunk_ids]

    return core_chunks


async def get_adjacent_chunks(
    session: AsyncSession, core_chunks: list[DocumentChunk]
) -> Iterable[DocumentChunk]:
    """
    Fetches the proximate chunks to the core_chunks (calculated by settings.N_CHUNKS_WINDOW).
    """
    final_chunks = []

    if core_chunks:
        adjacency_conditions = []

        for chunk in core_chunks:
            if chunk.document_chunk_index is not None:
                # For PDF and text files
                adjacency_conditions.append(
                    and_(
                        DocumentChunk.document_id == chunk.document_id,
                        DocumentChunk.document_chunk_index  # type: ignore
                        >= chunk.document_chunk_index - settings.N_CHUNKS_WINDOW,
                        DocumentChunk.document_chunk_index  # type: ignore
                        <= chunk.document_chunk_index + settings.N_CHUNKS_WINDOW,
                    )
                )
            else:
                # For image files
                adjacency_conditions.append(DocumentChunk.id == chunk.id)

        query_final = (
            select(DocumentChunk)
            .where(or_(*adjacency_conditions))
            .order_by(
                col(DocumentChunk.document_id).asc(),
                col(DocumentChunk.document_chunk_index).asc(),
            )
            .options(selectinload(DocumentChunk.document))  # type: ignore
        )

        final_chunks = (await session.execute(query_final)).scalars().all()

    return final_chunks


async def retrieval(
    session: AsyncSession,
    interaction: Interaction,
    raw_prompt: str,
    embedded_prompt: list[float],
) -> Iterable[DocumentChunk]:
    """
    Retrieves relevant core chunks AND their surrounding chunks
    """

    # Vector search
    query_vector = (
        select(DocumentChunk)
        .join(Document)
        .where(Document.interaction_id == interaction.id)
        .order_by(DocumentChunk.content_embedded.cosine_distance(embedded_prompt))  # type: ignore
        .limit(settings.N_CHUNKS_RETRIEVED * 2)
        # .options(selectinload(DocumentChunk.document))  # type: ignore
    )

    vector_chunks = (await session.execute(query_vector)).scalars().all()

    # Keyword search
    query_keyword = (
        select(DocumentChunk)
        .join(Document)
        .where(Document.interaction_id == interaction.id)
        .order_by(col(DocumentChunk.content_original).op("<->")(raw_prompt))
        .limit(settings.N_CHUNKS_RETRIEVED * 2)
    )

    keyword_chunks = (await session.execute(query_keyword)).scalars().all()

    # Merge
    core_chunks = RRF(vector_chunks, keyword_chunks)

    # Get adjacent chunks
    final_chunks = await get_adjacent_chunks(session, core_chunks)

    return final_chunks
