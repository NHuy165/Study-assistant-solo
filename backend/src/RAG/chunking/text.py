import asyncio
from abc import abstractmethod

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.ai_api import GlobalAPI
from backend.src.exceptions.core import ExceptionRequestValidation_400
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.miscellaneous.enums import DocumentType
from backend.src.RAG.chunking.base import DocumentExtractor, smart_splitter


class TextExtractor(DocumentExtractor):
    @classmethod
    @abstractmethod
    def verify(cls, file: UploadFile) -> bool:
        # === Content type === #
        if file.content_type is None:
            return False

        is_text = (
            file.content_type.startswith("text/")
            or file.content_type == "application/json"
        )
        is_generic = file.content_type == "application/octet-stream"

        if not (is_text or is_generic):
            return False

        # === Header === #
        header = file.file.read(512)
        file.file.seek(0)

        if not header:
            return False

        try:
            header.decode("utf-8")
            return True

        except UnicodeDecodeError:
            return False

    @classmethod
    @abstractmethod
    async def extract(
        cls, session: AsyncSession, file: UploadFile, document: Document
    ) -> None:
        # Reads the file
        text_bytes = await file.read()
        try:
            contents = text_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise ExceptionRequestValidation_400(
                "Invalid file format.\nAllowed formats are:\n- PDF\n- JPEG, PNGM, WEBP\n- Text files\nPlease recheck file extension and file contents."
            )

        if len(contents.strip()) == 0:
            return

        split_chunks = smart_splitter.split_text(contents)

        # Staging data
        prepared_chunks = []
        chunk_metadata = []

        for chunk_index, chunk_text in enumerate(split_chunks):
            embedding_content = (
                f"Source: {DocumentType.TEXT.value} file {document.name}:\n"
                + chunk_text
            )

            prepared_chunks.append(GlobalAPI.embed(embedding_content))
            chunk_metadata.append(
                {
                    "content": chunk_text,
                    "index": chunk_index,
                }
            )

        if prepared_chunks:
            # Mass awaiting
            vectors = await asyncio.gather(*prepared_chunks)

            for metadata, vector in zip(chunk_metadata, vectors):
                embedded_chunk = DocumentChunk(
                    content_original=metadata["content"],
                    content_embedded=vector,
                    document_chunk_index=metadata["index"],
                    document=document,
                )
                session.add(embedded_chunk)

        await session.commit()
