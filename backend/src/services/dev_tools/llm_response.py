from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models_schema.interaction.interaction import Interaction
from backend.src.models_schema.llm_response.llm_response import (
    LLMResponse,
    LLMResponseInput,
)
from backend.src.models_schema.user.user import User

# ----- CREATE ----- #


async def mock_create_llm_response(
    user: User,
    session: AsyncSession,
    current_datetime: datetime,
    llm_response_input: LLMResponseInput,
    interaction: Interaction,
) -> LLMResponse:
    # Saving response
    llm_response = LLMResponse(
        prompt=llm_response_input.prompt,
        answer=f"Reply to: {llm_response_input.prompt}",
        interaction=interaction,
        created_at=current_datetime,
    )

    session.add(llm_response)
    await session.commit()
    # await session.refresh(llm_response)

    return llm_response
