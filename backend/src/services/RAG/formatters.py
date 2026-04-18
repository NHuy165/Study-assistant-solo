from abc import ABC, abstractmethod
from typing import Iterable

from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.enums import DocumentType
from backend.src.models_schema.llm_response import LLMResponse
from backend.src.services.RAG.stitch import chunks_stitcher

# ----- CHUNK FORMAT ----- #


class ContentFormatter(ABC):
    @classmethod
    @abstractmethod
    def format(
        cls, index: int, head_chunk: DocumentChunk, page_end: int, stitched_content: str
    ) -> str:
        pass


class PDFFormatter(ContentFormatter):
    @classmethod
    def format(
        cls, index: int, head_chunk: DocumentChunk, page_end: int, stitched_content: str
    ) -> str:
        assert head_chunk.document_page_num is not None

        return f"""Context {index}:
Source: 
- Document name: {head_chunk.document.name}
- Type: {DocumentType.PDF.value}
- Page: {head_chunk.document_page_num + head_chunk.document.page_starts_at} -> {page_end}
Contents:
{stitched_content}
"""


class ImageFormatter(ContentFormatter):
    @classmethod
    def format(
        cls, index: int, head_chunk: DocumentChunk, page_end: int, stitched_content: str
    ) -> str:
        return f"""Context {index}:
Source:
- Document name: {head_chunk.document.name}
- Type: {DocumentType.IMAGE.value}
Contents:
{stitched_content}
"""


class TextFormatter(ContentFormatter):
    @classmethod
    def format(
        cls, index: int, head_chunk: DocumentChunk, page_end: int, stitched_content: str
    ) -> str:
        document = head_chunk.document
        return f"""Context {index}:
Source:
- Document name: {document.name}
- Type: {DocumentType.TEXT.value}
Contents:
{stitched_content}
"""


FORMATTERS: dict[DocumentType, type[ContentFormatter]] = {
    DocumentType.PDF: PDFFormatter,
    DocumentType.IMAGE: ImageFormatter,
    DocumentType.TEXT: TextFormatter,
}


def stitched_content_formatter(
    index: int, head_chunk: DocumentChunk, page_end: int, stitched_content: str
) -> str:
    """
    Converts a content block (a stitched block of chunks) into text depending on its document type.
    """
    document = head_chunk.document

    formatter_class = FORMATTERS.get(document.type)

    if formatter_class is None:
        raise Exception("Unknown document type")

    return formatter_class.format(index, head_chunk, page_end, stitched_content)


def chunks_formatter(chunks: Iterable[DocumentChunk]) -> str:
    """
    Converts document chunks into text (through stitching and formatting).
    """
    stitched_contents = chunks_stitcher(chunks)

    formatted_chunks = "\n\n".join(
        stitched_content_formatter(i, *content_block)
        for i, content_block in enumerate(stitched_contents, start=1)
    )

    return formatted_chunks


# ----- CONVERSATION FORMAT ----- #


def singular_conversation_formatter(index: int, conversation: LLMResponse) -> str:
    return f"""Conversation {index}:
User query: {conversation.prompt}
Model answer: {conversation.answer}
"""


def conversations_formatter(conversations: Iterable[LLMResponse]):
    formatted_conversations = "\n\n".join(
        singular_conversation_formatter(i, conv)
        for i, conv in enumerate(conversations, start=1)
    )

    return formatted_conversations
