from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from backend.src.core.ai_api import GoogleAPI
from backend.src.core.config import settings
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.llm_response import (
    LLMResponse,
    LLMResponseInput,
)
from backend.src.services.RAG.augmentation import prompt_augmentation
from backend.src.services.RAG.retrieval import retrieval

# ----- CREATE ----- #


async def create_llm_response(
    session: AsyncSession,
    llm_response_input: LLMResponseInput,
    interaction: Interaction,
) -> LLMResponse:

    # Retrieval
    embedded_prompt = GoogleAPI.embed(llm_response_input.prompt)
    document_chunks = await retrieval(session, interaction, embedded_prompt)

    past_conversations = await read_llm_responses(
        session, interaction, settings.N_PAST_CONVERSATIONS
    )

    # Augmentation
    final_prompt = prompt_augmentation(
        document_chunks, past_conversations, llm_response_input.prompt
    )

    # Generation
    answer = GoogleAPI.generate_content(final_prompt)

    # Saving response
    llm_response = LLMResponse(
        prompt=llm_response_input.prompt,
        answer=answer,
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
