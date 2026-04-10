from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import Column, col, select

from backend.src.core.config import ai_client, settings
from backend.src.exceptions.core import ExceptionRequest_400
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.llm_response import (
    LLMResponse,
    LLMResponseInput,
)
from backend.src.services.document_chunk import embed

# ----- CREATE ----- #


def prompt_augmentation(chunks: list[DocumentChunk], prompt: str):

    context = "\n".join(
        [
            f"Document {c.document.name}. Page {c.document_page_num}:\n{c.content_original}"
            for c in chunks
        ]
    )

    final_prompt = f"""
    You are a helpful study assistant for primary school students. Answer the question using ONLY the provided context.
    
    If the answer is not in the context, say "I don't know" (adapt this to other languages).
    
    Question:
    {prompt}
    
    Context:
    {context}
    
    Answer:
    """

    return final_prompt


async def create_llm_response(
    session: AsyncSession,
    llm_response_input: LLMResponseInput,
    interaction: Interaction,
) -> LLMResponse:
    embedded_prompt = embed(llm_response_input.prompt)

    # Retrieval
    query = (
        select(DocumentChunk)
        .join(Document)
        .where(Document.interaction_id == interaction.id)
        .order_by(DocumentChunk.content_embedded.cosine_distance(embedded_prompt))  # type: ignore
        .limit(settings.N_CHUNKS_RETRIEVED)
        .options(selectinload(DocumentChunk.document))  # type: ignore
    )

    document_chunks = (await session.execute(query)).scalars().all()

    # Augmentation
    final_prompt = prompt_augmentation(list(document_chunks), llm_response_input.prompt)

    # Generation
    response = ai_client.models.generate_content(
        model=settings.ANSWER_MODEL,
        contents=final_prompt,
    )

    # Validation
    if response.text is None:
        raise ExceptionRequest_400(
            "A response could not be generated. Please recheck your question."
        )

    # Saving response
    llm_response = LLMResponse(
        prompt=llm_response_input.prompt,
        answer=response.text,
        interaction=interaction,
    )

    session.add(llm_response)
    await session.commit()
    await session.refresh(llm_response)

    return llm_response


# ----- READ ----- #


async def read_llm_responses(
    session: AsyncSession, interaction: Interaction, limit: int | None
) -> list[LLMResponse]:
    query = (
        select(LLMResponse)
        .where(LLMResponse.interaction_id == interaction.id)
        .order_by(col(LLMResponse.created_at).desc())
    )
    if limit is not None:
        query = query.limit(limit)

    llm_responses = (await session.execute(query)).scalars().all()

    return list(llm_responses)


# ----- UPDATE ----- #
# ----- DELETE ----- #
