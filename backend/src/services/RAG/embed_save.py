from abc import ABC, abstractmethod

from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.ai_api import GoogleAPI
from backend.src.core.config import settings
from backend.src.exceptions.core import ExceptionRequest_400
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.enums import DocumentType

# ----- CHUNKING ----- #

smart_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.DEFAULT_CHUNK_SIZE,
    chunk_overlap=settings.DEFAULT_CHUNK_OVERLAP,
    separators=["\n\n", "\n", ".", " ", ""],
)

# ----- EXTRACT AND SAVE ----- #


class DocumentExtractor(ABC):
    @classmethod
    @abstractmethod
    def verify(cls, file: UploadFile) -> bool:
        """
        Verifies whether a file is of a certain format.
        """
        pass

    @classmethod
    @abstractmethod
    async def extract(
        cls, session: AsyncSession, file: UploadFile, document: Document
    ) -> None:
        """
        Extracts and saves chunks.
        """
        pass


class PdfExtractor(DocumentExtractor):
    @classmethod
    def verify(cls, file: UploadFile) -> bool:
        # === Content type === #
        if file.content_type != "application/pdf":
            return False

        # === Header === #
        header = file.file.read(5)
        file.file.seek(0)

        if header != b"%PDF-":
            return False

        return True

    @classmethod
    async def extract(
        cls, session: AsyncSession, file: UploadFile, document: Document
    ) -> None:
        reader = PdfReader(file.file)

        chunk_index = 0

        # Iterating over document pages
        for page_num, page_contents in enumerate(reader.pages):
            page_text = page_contents.extract_text()

            if len(page_text.strip()) == 0:
                continue

            # Chopping text in 1 page into chunks
            split_chunks = smart_splitter.split_text(page_text)

            for chunk_text in split_chunks:
                embedding_content = (
                    f"Source: {DocumentType.PDF.value} file {document.name}, page {page_num + document.page_starts_at}:\n"
                    + chunk_text
                )

                prepared_chunk = DocumentChunk(
                    content_original=chunk_text,
                    content_embedded=GoogleAPI.embed(embedding_content),
                    document_page_num=page_num,
                    document_chunk_index=chunk_index,
                    document=document,
                )

                session.add(prepared_chunk)

                chunk_index += 1

        await session.commit()


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
        image_description = await GoogleAPI.describe_image(file)

        embedding_content = (
            f"Source: {DocumentType.IMAGE.value} file {document.name}:\n"
            + image_description
        )

        prepared_chunk = DocumentChunk(
            content_original=f"[IMAGE DESCRIPTION]: {image_description}",
            content_embedded=GoogleAPI.embed(embedding_content),
            document=document,
        )

        session.add(prepared_chunk)
        await session.commit()


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
            raise ExceptionRequest_400(
                "Invalid file format.\nAllowed formats are:\n- PDF\n- JPEG, PNGM, WEBP\n- Text files\nPlease recheck file extension and file contents."
            )

        if len(contents.strip()) == 0:
            return

        split_chunks = smart_splitter.split_text(contents)

        for chunk_index, chunk_text in enumerate(split_chunks):
            embedding_content = (
                f"Source: {DocumentType.TEXT.value} file {document.name}:\n"
                + chunk_text
            )

            prepared_chunk = DocumentChunk(
                content_original=chunk_text,
                content_embedded=GoogleAPI.embed(embedding_content),
                document_chunk_index=chunk_index,
                document=document,
            )

            session.add(prepared_chunk)

        await session.commit()
