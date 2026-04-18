from backend.src.core.ai_api import GlobalAPI
from backend.src.core.prompts import PROMPT_REWRITE_BASE


async def rewrite_prompt(raw_prompt: str, context_conversations: str) -> str:
    prompt_rewrite = PROMPT_REWRITE_BASE.format(
        context_conversations=context_conversations, raw_prompt=raw_prompt
    )

    rewritten_prompt = await GlobalAPI.generate_content(prompt_rewrite)

    return rewritten_prompt
