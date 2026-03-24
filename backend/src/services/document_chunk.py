from fastapi import UploadFile
from google.genai import types
from pypdf import PdfReader
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.config import ai_client, settings
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk

# ----- CREATE ----- #


def embed(text: str) -> list[float]:
    """
    Embeds ONE CHUNK of text into a 768-D vector.
    """
    embedded = ai_client.models.embed_content(
        model=settings.EMBED_MODEL,
        contents=text,
        # Content is truncated from 3072-D to 768-D
        config=types.EmbedContentConfig(
            output_dimensionality=768,
        ),
    )

    # Let this throw an internal error if wrong
    assert embedded.embeddings is not None
    assert isinstance(embedded.embeddings[0].values, list)

    return embedded.embeddings[0].values


async def save_document_chunks(
    session: AsyncSession, file: UploadFile, document: Document, page_offset: int
) -> None:
    reader = PdfReader(file.file)

    chunk_index = 0

    # Iterating over document pages
    for page_num, page_contents in enumerate(reader.pages):
        page_text = page_contents.extract_text()

        if len(page_text.strip()) == 0:
            continue

        pos = 0

        # Chopping text in 1 page into chunks
        while pos < len(page_text):
            chunk_text = page_text[pos : pos + settings.DEFAULT_CHUNK_SIZE]

            prepared_chunk = DocumentChunk(
                content_original=chunk_text,
                content_embedded=embed(chunk_text),
                document_page_num=page_num + page_offset,
                document_chunk_index=chunk_index,
                document=document,
            )

            session.add(prepared_chunk)

            # Moving position forwards
            chunk_index += 1
            pos += settings.DEFAULT_CHUNK_SIZE - settings.DEFAULT_CHUNK_OVERLAP

    await session.commit()


# ----- READ ----- #
# ----- UPDATE ----- #
# ----- DELETE ----- #
