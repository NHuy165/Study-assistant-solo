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
    Chops textual data into chunks with an overlap between chunks.
    """
    result = []
    pos = 0

    while pos < len(text):
        result.append(text[pos : pos + chunk_size])
        pos += chunk_size - overlap

    return result


def process_pdf(file_name: str, page_offset: int = 0) -> list[dict]:
    correct_path = Path(__file__).parent / "NEED_READ_FILES_GO_HERE" / file_name
    reader = PdfReader(correct_path)

    result = []
    chunk_index = 0

    for page_num, page_contents in enumerate(reader.pages):
        page_text = page_contents.extract_text()

        # Skip empty
        if page_text.strip() == 0:
            continue

        # Page chopping
        chunks = get_overlapping_chunks(
            text=page_text,
            chunk_size=500,
            overlap=50,
        )

        for chunk in chunks:
            content_embeddings = embed(chunk).embeddings
            if content_embeddings is None:
                raise  # CHANGE THIS LATER

            prepared_chunk = {
                "content_original": chunk,
                "content_embedded": content_embeddings[0].values,
                "document_name": file_name,
                "document_page_num": page_num + page_offset,
                "document_chunk_index": chunk_index,
            }
            result.append(prepared_chunk)
            chunk_index += 1

    return result
