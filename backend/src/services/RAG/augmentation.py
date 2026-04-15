from typing import Iterable

from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.enums import DocumentType
from backend.src.models_schema.llm_response import LLMResponse
from backend.src.services.RAG.formatters import (
    conversations_formatter,
    stitched_content_formatter,
)

# ----- CHUNK STITCH ----- #


def stitch(
    chunks: list[DocumentChunk], stitched_contents: list[tuple[DocumentChunk, int, str]]
) -> None:
    """
    Stitches all chunks in ONE document, watching for gaps.
    """
    # Set up current stitched content container (current_doc_text)
    head_chunk = chunks[0]
    is_pdf = head_chunk.document.type.value == "PDF"
    current_doc_text = []

    if is_pdf:
        start_page = (
            head_chunk.document_page_num + head_chunk.document.page_starts_at  # type: ignore
        )
        current_doc_text.append(f"[--- Page {start_page} ---]\n\n")  # type: ignore
    current_doc_text.append(head_chunk.content_original)

    # Loops over chunks, watching out for gaps
    for j in range(1, len(chunks)):
        # If gap, finalize and append
        if chunks[j].document_chunk_index != chunks[j - 1].document_chunk_index + 1:  # type: ignore
            block_content = "".join(current_doc_text)
            end_page = (
                chunks[j - 1].document_page_num + head_chunk.document.page_starts_at  # type: ignore
                if head_chunk.document.type.value == "PDF"
                else 0
            )
            stitched_contents.append((head_chunk, end_page, block_content))

            head_chunk = chunks[j]
            current_doc_text = []

            if is_pdf:
                start_page = (
                    head_chunk.document_page_num  # type: ignore
                    + head_chunk.document.page_starts_at
                )
                current_doc_text.append(f"[--- Page {start_page} ---]\n\n")

        # If no gap, but we just crossed a page
        elif is_pdf and chunks[j].document_page_num != chunks[j - 1].document_page_num:
            new_page = (
                chunks[j].document_page_num + head_chunk.document.page_starts_at  # type: ignore
            )
            current_doc_text.append(f"\n\n[--- Page {new_page} ---]\n\n")

        current_doc_text.append(chunks[j].content_original)

    # Final save
    block_content = "".join(current_doc_text)
    end_page = (
        chunks[-1].document_page_num + head_chunk.document.page_starts_at  # type: ignore
        if head_chunk.document.type.value == "PDF"
        else 0
    )
    stitched_contents.append((head_chunk, end_page, block_content))


def chunks_stitcher(
    document_chunks: Iterable[DocumentChunk],
) -> list[tuple[DocumentChunk, int, str]]:
    """
    Receives an ordered list of document chunks, stitch them together.
    Returns a list of content blocks containing: The header chunk, the page end number (offset considered), the stitched together contents.
    """
    stitched_contents: list[tuple[DocumentChunk, int, str]] = []

    grouped_docs: dict[int, list[DocumentChunk]] = dict()  # Groups non-image chunks
    for chunk in document_chunks:
        # Document is image
        if chunk.document.type == DocumentType.IMAGE:
            stitched_contents.append((chunk, 0, chunk.content_original))

        # Document is not image
        else:
            grouped_docs.setdefault(chunk.document.id, []).append(chunk)  # type: ignore

    # Stitch adjacent chunks in a document, watches for gaps
    for chunks in grouped_docs.values():
        stitch(chunks, stitched_contents)

    return stitched_contents


# ----- AUGMENTATION ----- #


PROMPT_BASE = """=== PURPOSE AND SCOPE ===
You are a friendly, encouraging, and highly accurate Study Assistant tailored for Vietnamese primary school students (Grades 1 to 5). 
Your core subjects are Mathematics, Vietnamese (Literature/Reading), and English.

=== KNOWLEDGE PRIORITY & RULES ===
The data used when answering questions follows the following priority system. Note that the priority system ONLY applies to data usage if you ARE answering the question.
1. PROVIDED CONTEXT (HIGHEST PRIORITY): `PROVIDED CONTEXT` is the information that the user sent you in the current interaction. You must base your answers primarily on the `PROVIDED CONTEXT`. If the context demonstrates a specific teaching method, rule, or format, you MUST follow it exactly, as this reflects the student's actual school curriculum. Unless, of course, the method is BLATANTLY wrong, in which case either follow it or warn the user about its inaccuracy, or do not follow it at all.
2. SUPPLEMENTAL KNOWLEDGE (MEDIUM PRIORITY): If the context does not contain the answer, you may use `SUPPLEMENTAL KNOWLEDGE`, containing handpicked documents by the developers of this program, which have a high chance of revelancy to your purpose.
3. INTERNAL KNOWLEDGE (LOW PRIORITY): If the answer does not lie in the provided context above, you may use your internal LLM knowledge, but strictly limit your explanation to the Vietnamese Grade 1-5 academic level.
4. PAST CONVERSATIONS: You may be passed a certain number of your most recent conversations with the user. This is done automatically and may or may not contain any relevant information to the current question. The conversations are indexed so that the lower the number, the more recent the conversation (Conversation 1 is your last conversation).

=== TONE & PERSONA ===
- Always respond in Vietnamese, unless specified otherwise by the student or if doing so is necessary (for example, when teaching English). 
- Use a gentle, supportive, and pedagogical tone appropriate for young children. The Vietnamese pronouns you will be using are "Mình/bạn".
- On citing information from `PROVIDED CONTEXT`. It is advised to mention the 'Source' information included with the context. This should be done discreetly to avoid cluttering the main information and may be skipped depending on the user's preferences.

=== BOUNDARIES & GUARDRAILS ===
Before answering ANY question or reading ANY context, you must evaluate the topic against these boundaries. These rules override all other instructions.
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


def prompt_augmentation(
    document_chunks: Iterable[DocumentChunk],
    context_conversations: str,
    prompt: str,
):
    # Augmenting context
    stitched_contents = chunks_stitcher(document_chunks)

    context_document = "\n\n".join(
        stitched_content_formatter(i, *content_block)
        for i, content_block in enumerate(stitched_contents, start=1)
    )

    # Augmented prompt
    final_prompt = PROMPT_BASE.format(
        context_document=context_document,
        context_conversations=context_conversations,
        prompt=prompt,
    )

    return final_prompt
