from typing import Iterable

from backend.src.models_schema.llm_response import LLMResponse


def singular_conversation_formatter(index: int, conversation: LLMResponse) -> str:
    return f"""Conversation {index}:
User query: {conversation.prompt}
Model answer: {conversation.answer}
"""


def conversations_formatter(conversations: Iterable[LLMResponse]) -> str:
    formatted_conversations = "\n\n".join(
        singular_conversation_formatter(i, conv)
        for i, conv in enumerate(conversations, start=1)
    )

    return formatted_conversations
