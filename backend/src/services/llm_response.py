from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from backend.src.core.ai_api import GlobalAPI
from backend.src.core.config import settings
from backend.src.models_schema.augmentation_params import AnswerGenerationParams
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.llm_response import (
    LLMResponse,
    LLMResponseInput,
)
from backend.src.services.RAG.augmentation import answer_generation_augmentation
from backend.src.services.RAG.formatters import (
    chunks_formatter,
    conversations_formatter,
)
from backend.src.services.RAG.retrieval import retrieval
from backend.src.services.RAG.rewrite import rewrite_prompt

# ----- CREATE ----- #


async def create_llm_response(
    session: AsyncSession,
    llm_response_input: LLMResponseInput,
    interaction: Interaction,
) -> LLMResponse:
    # Gets past conversations
    past_conversations = await read_llm_responses(
        session, interaction, settings.N_PAST_CONVERSATIONS
    )
    formatted_past_conversations = conversations_formatter(past_conversations)

    # Retrieval (using the rewritten prompt)
    rewritten_prompt = await rewrite_prompt(
        llm_response_input.prompt, formatted_past_conversations
    )
    embedded_prompt = await GlobalAPI.embed(rewritten_prompt)
    document_chunks = await retrieval(
        session=session,
        interaction=interaction,
        raw_prompt=rewritten_prompt,
        embedded_prompt=embedded_prompt,
    )
    formatted_chunks = chunks_formatter(document_chunks)

    # Augmentation
    augmentation_params = AnswerGenerationParams(
        prompt=llm_response_input.prompt,
        context_conversations=formatted_past_conversations,
        context_document=formatted_chunks,
    )
    final_prompt = answer_generation_augmentation(augmentation_params)

    # Generation
    answer = await GlobalAPI.generate_content(final_prompt)

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
