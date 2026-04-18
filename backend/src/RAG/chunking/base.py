from abc import ABC, abstractmethod

from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.config import settings
from backend.src.models_schema.document import Document

smart_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.DEFAULT_CHUNK_SIZE,
    chunk_overlap=settings.DEFAULT_CHUNK_OVERLAP,
    separators=["\n\n", "\n", ".", " ", ""],
)


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
