from pathlib import Path

from google.genai import types
from pypdf import PdfReader

from backend.src.core.config import ai_client
from backend.src.core.database import SessionDep
from backend.src.models_schema.document_chunk import DocumentChunk


def embed(text: str):
    """
    Embeds text into a 768-D vector.
    """
    result = ai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        # Content is truncated from 3072-D to 768-D
        config=types.EmbedContentConfig(
            output_dimensionality=768,
        ),
    )
    return result


def get_overlapping_chunks(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    """
    Chops textual data into chunks of size {chunk_size} and an overlap between chunks of {overlap}.
    """
    result = []
    pos = 0

    while pos < len(text):
        result.append(text[pos : pos + chunk_size])
        pos += chunk_size - overlap

    return result
