import asyncio

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

        def process():
            reader = PdfReader(file.file)

            # Staging data
            prepared_chunks: list[str] = []
            chunk_metadata = []

            # Iterating over document pages
            chunk_index = 0

            for page_num, page_contents in enumerate(reader.pages):
                page_text = page_contents.extract_text()

                if not page_text or len(page_text.strip()) == 0:
                    continue

                # Chopping text in 1 page into chunks
                split_chunks = smart_splitter.split_text(page_text)

                for chunk_text in split_chunks:
                    # Adding metadata to chunk
                    embedding_content = (
                        f"Source: {DocumentType.PDF.value} file {document.name}, page {page_num + document.page_starts_at}:\n"
                        + chunk_text
                    )

                    prepared_chunks.append(embedding_content)
                    chunk_metadata.append(
                        {
                            "content": chunk_text,
                            "page": page_num,
                            "index": chunk_index,
                        }
                    )

                    chunk_index += 1

            return prepared_chunks, chunk_metadata

        prepared_chunks, chunk_metadata = await asyncio.to_thread(process)

        # Embedding all data
        if prepared_chunks:
            vectors = await GlobalAPI.mass_embed(prepared_chunks)

            embedded_chunks = [
                DocumentChunk(
                    content_original=metadata["content"],
                    content_embedded=vector,
                    document_page_num=metadata["page"],
                    document_chunk_index=metadata["index"],
                    document=document,
                )
                for metadata, vector in zip(chunk_metadata, vectors)
            ]

            session.add_all(embedded_chunks)
