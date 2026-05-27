from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.ai_api import GlobalAPI
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.miscellaneous.enums import DocumentType
from backend.src.RAG.chunking.base import DocumentExtractor


class ImageExtractor(DocumentExtractor):
    @classmethod
    def verify(cls, file: UploadFile) -> bool:
        # === Content type === #
        allowed_types = {"image/jpeg", "image/png", "image/webp"}
        if file.content_type not in allowed_types:
            return False

        # === Header === #
        header = file.file.read(12)
        file.file.seek(0)

        is_jpeg = header.startswith(b"\xff\xd8\xff")
        is_png = header.startswith(b"\x89PNG\r\n\x1a\n")
        is_webp = header.startswith(b"RIFF") and header[8:12] == b"WEBP"

        if not (is_jpeg or is_png or is_webp):
            return False

        return True

    @classmethod
    async def extract(
        cls, session: AsyncSession, file: UploadFile, document: Document
    ) -> None:
        # Reads the image using the model
        image_description = await GlobalAPI.caption_image(file)

        embedding_content = (
            f"Source: {DocumentType.IMAGE.value} file {document.name}:\n"
            + image_description
        )

        prepared_chunk = DocumentChunk(
            content_original=f"[IMAGE DESCRIPTION]: {image_description}",
            content_embedded=await GlobalAPI.embed(embedding_content),
            document=document,
        )

        session.add(prepared_chunk)
