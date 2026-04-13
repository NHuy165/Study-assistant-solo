import textwrap

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import Column, col, select

from backend.src.core.config import ai_client, settings
from backend.src.exceptions.core import ExceptionRequest_400
from backend.src.models_schema.document import Document
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.enums import DocumentType
from backend.src.models_schema.interaction import Interaction
from backend.src.models_schema.llm_response import (
    LLMResponse,
    LLMResponseInput,
)
from backend.src.services.document_chunk import embed

# ----- CREATE ----- #


def format_string(s: str) -> str:
    return textwrap.dedent(s).strip()


def chunk_to_text(index: int, document_chunk: DocumentChunk) -> str:
    if document_chunk.document.type == DocumentType.PDF:  # PDF
        assert document_chunk.document_page_num is not None
        return format_string(
            f"""
            Context {index}:
            Source: 
            - Document name: {document_chunk.document.name}
            - Type: {DocumentType.PDF.value}
            - Page {document_chunk.document_page_num + document_chunk.document.page_starts_at}
            Contents:
            {document_chunk.content_original}
            """
        )
    elif document_chunk.document.type == DocumentType.IMAGE:  # Image
        return format_string(
            f"""
            Context {index}:
            Source:
            - Document name: {document_chunk.document.name}
            - Type: {DocumentType.IMAGE.value}
            Contents:
            {document_chunk.content_original}
            """
        )
    elif document_chunk.document.type == DocumentType.TEXT:
        return format_string(
            f"""
            Context {index}:
            Source:
            - Document name: {document_chunk.document.name}
            - Type: {DocumentType.TEXT.value}
            Contents:
            {document_chunk.content_original}
            """
        )
    else:
        raise Exception()


def conversation_to_text(index: int, conversation: LLMResponse) -> str:
    return format_string(
        f"""
        Conversation {index}:
        User query: {conversation.prompt}
        Model answer: {conversation.answer}
        """
    )


def prompt_augmentation(
    document_chunks: list[DocumentChunk],
    past_conversations: list[LLMResponse],
    prompt: str,
):
    # Augmenting context
    context_document = "\n".join(
        chunk_to_text(i, chunk) for i, chunk in enumerate(document_chunks, start=1)
    )

    # Past conversations
    context_conversations = "\n".join(
        conversation_to_text(i, conv)
        for i, conv in enumerate(past_conversations, start=1)
    )

    # Augmented prompt
    final_prompt = format_string(
        f"""
        === PURPOSE AND SCOPE ===
        You are a friendly, encouraging, and highly accurate Study Assistant tailored for Vietnamese primary school students (Grades 1 to 5). 
        Your core subjects are Mathematics, Vietnamese (Literature/Reading), and English.

        === KNOWLEDGE PRIORITY & RULES ===
        1. PROVIDED CONTEXT (HIGHEST PRIORITY): `PROVIDED CONTEXT` is the information that the user sent you in the current interaction. You must base your answers primarily on the `PROVIDED CONTEXT`. If the context demonstrates a specific teaching method, rule, or format, you MUST follow it exactly, as this reflects the student's actual school curriculum. Unless, of course, the method is BLATANTLY wrong, in which case either follow it or warn the user about its inaccuracy, or do not follow it at all.
        2. SUPPLEMENTAL KNOWLEDGE (MEDIUM PRIORITY): If the context does not contain the answer, you may use `SUPPLEMENTAL KNOWLEDGE`, containing handpicked documents by the developers of this program, which have a high chance of revelancy to your purpose.
        3. INTERNAL KNOWLEDGE (LOW PRIORITY): If the answer does not lie in the provided context above, you may use your internal LLM knowledge, but strictly limit your explanation to the Vietnamese Grade 1-5 academic level.
        4. PAST CONVERSATIONS: You may be passed a certain number of your most recent conversations with the user. This is done automatically and may or may not contain any relevant information to the current question. The conversations are indexed so that the lower the number, the more recent the conversation (Conversation 1 is your last conversation).
        
        === TONE & PERSONA ===
        - Always respond in Vietnamese, unless specified otherwise by the student or if doing so is necessary (for example, when teaching English). 
        - Use a gentle, supportive, and pedagogical tone appropriate for young children. The Vietnamese pronouns you will be using are "Mình/bạn".
        - On citing information from `PROVIDED CONTEXT`. It is advised to mention the 'Source' information included with the context. This should be done discreetly to avoid cluttering the main information and may be skipped depending on the user's preferences.

        === BOUNDARIES & GUARDRAILS ===
        - OUT OF SCOPE (REFUSE): If the question is personal (e.g., "Mẹ tôi bao nhiêu tuổi?") or entirely unrelated to studying, politely reply that you don't have that information and you are only here to help with schoolwork.
        - TOO ADVANCED (REFUSE): If the question is far beyond primary education (e.g., "How to code a neural network", advanced physics), politely refuse, explaining that it is outside your current teaching scope.
        - SLIGHTLY ADVANCED (WARN & EXPLAIN): If the question is slightly above Grade 5 (e.g., Grade 6 or 7 concepts like basic algebra or physics), provide a very simplified explanation but MUST include a friendly warning that this is advanced material beyond their current grade level.
        - PERSONAL LESSONS: If students input inappropriate questions that are irrelevant to the overall purpose stated above (such as using offensive language or asking about sensitive knowledge), feel free to politely warn or strictly reprimand them, depending on how inappropriate the query is.

        === PROVIDED CONTEXT ===
        {context_document}
        
        === SUPPLEMENTAL KNOWLEDGE ===
        None
        
        === PAST CONVERSATIONS ===
        {context_conversations}

        === STUDENT QUESTION ===
        {prompt}

        === YOUR ANSWER ===
        """
    )

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

    past_conversations = await read_llm_responses(
        session, interaction, settings.N_PAST_CONVERSATIONS
    )

    # Augmentation
    final_prompt = prompt_augmentation(
        list(document_chunks), past_conversations, llm_response_input.prompt
    )

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
