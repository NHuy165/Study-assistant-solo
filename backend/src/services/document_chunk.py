from fastapi import UploadFile
from google.genai import types
from pypdf import PdfReader
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.config import ai_client, settings
from backend.src.exceptions.core import ExceptionRequest_400
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.enums import DocumentType

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


async def save_pdf_chunks(
    session: AsyncSession, file: UploadFile, document: Document
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

            embedding_content = (
                f"Source: {DocumentType.PDF.value} file {document.name}, page {page_num + document.page_starts_at}:\n"
                + chunk_text
            )

            prepared_chunk = DocumentChunk(
                content_original=chunk_text,
                content_embedded=embed(embedding_content),
                document_page_num=page_num,
                document_chunk_index=chunk_index,
                document=document,
            )

            session.add(prepared_chunk)

            # Moving position forwards
            chunk_index += 1
            pos += settings.DEFAULT_CHUNK_SIZE - settings.DEFAULT_CHUNK_OVERLAP

    await session.commit()


async def save_image_chunks(
    session: AsyncSession, file: UploadFile, document: Document
) -> None:
    # Extracting information from the image
    image_bytes = await file.read()

    prompt_text = """
    Extract all readable text from this image exactly as written. 
    Then, describe the layout, charts, figures, subjects, and any data points in exhaustive detail.
    """

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=file.content_type,  # type: ignore
    )

    # Reads the image using the model
    response = ai_client.models.generate_content(
        model=settings.ANSWER_MODEL,
        contents=[prompt_text, image_part],
    )

    image_description = response.text
    # Validation
    if image_description is None:
        raise ExceptionRequest_400("Image could not be saved properly.")

    embedding_content = (
        f"Source: {DocumentType.IMAGE.value} file {document.name}:\n"
        + image_description
    )

    prepared_chunk = DocumentChunk(
        content_original=f"[IMAGE DESCRIPTION]: {image_description}",
        content_embedded=embed(embedding_content),
        document=document,
    )

    session.add(prepared_chunk)
    await session.commit()


async def save_text_chunks(
    session: AsyncSession, file: UploadFile, document: Document
) -> None:
    # Reads the file
    text_bytes = await file.read()
    try:
        contents = text_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ExceptionRequest_400(
            "Invalid file format.\nAllowed formats are:\n- PDF\n- JPEG, PNGM, WEBP\n- Text files\nPlease recheck file extension and file contents."
        )

    if len(contents.strip()) == 0:
        return

    chunk_index = 0
    pos = 0

    while pos < len(contents):
        chunk_text = contents[pos : pos + settings.DEFAULT_CHUNK_SIZE]

        embedding_content = (
            f"Source: {DocumentType.TEXT.value} file {document.name}:\n" + chunk_text
        )

        prepared_chunk = DocumentChunk(
            content_original=chunk_text,
            content_embedded=embed(embedding_content),
            document_chunk_index=chunk_index,
            document=document,
        )

        session.add(prepared_chunk)

        chunk_index += 1
        pos += settings.DEFAULT_CHUNK_SIZE - settings.DEFAULT_CHUNK_OVERLAP

    await session.commit()


# ----- READ ----- #
# ----- UPDATE ----- #
# ----- DELETE ----- #
