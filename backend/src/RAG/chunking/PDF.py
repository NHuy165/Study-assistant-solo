from fastapi import UploadFile
from pypdf import PdfReader
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.ai_api import GlobalAPI
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.miscellaneous.enums import DocumentType
from backend.src.RAG.chunking.base import DocumentExtractor, smart_splitter


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
                    content_embedded=await GlobalAPI.embed(embedding_content),
                    document_page_num=page_num,
                    document_chunk_index=chunk_index,
                    document=document,
                )

                session.add(prepared_chunk)

                chunk_index += 1

        await session.commit()
