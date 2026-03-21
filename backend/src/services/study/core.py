from pathlib import Path

from pypdf import PdfReader
from sqlmodel import text

from backend.src.core.config import ai_client, settings
from backend.src.core.database import SessionDep
from backend.src.models_schema.document_chunk import DocumentChunk
from backend.src.models_schema.study import ModelPrompt, ModelResponse
from backend.src.services.study.utils import embed, get_overlapping_chunks


# NEEDS OPTIMIZING
async def save_chunks_service(
    session: SessionDep, file_name: str, page_offset: int = 0
):
    correct_path = Path(__file__).parent / "NEED_READ_FILES_GO_HERE" / file_name
    reader = PdfReader(correct_path)

    chunk_index = 0

    for page_num, page_contents in enumerate(reader.pages):
        page_text = page_contents.extract_text()

        # Skips empty
        if len(page_text.strip()) == 0:
            continue

        # Chops page into chunks
        chunks = get_overlapping_chunks(
            text=page_text,
            chunk_size=settings.DEFAULT_CHUNK_SIZE,
            overlap=settings.DEFAULT_CHUNK_OVERLAP,
        )

        for chunk in chunks:
            prepared_chunk = DocumentChunk(
                content_original=chunk,
                content_embedded=embed(chunk).embeddings[0].values,  # type: ignore
                document_name=file_name,
                document_page_num=page_num + page_offset,
                document_chunk_index=chunk_index,
            )

            session.add(prepared_chunk)
            chunk_index += 1

    await session.commit()


# NEEDS OPTIMIZING
async def answer_query_service(
    session: SessionDep, prompt: ModelPrompt
) -> ModelResponse:
    embedded_prompt_vector = embed(prompt.question).embeddings[0].values  # type: ignore

    # RAG vector searching
    query = text("""
    SELECT content_original, document_name, document_page_num, document_chunk_index
    FROM "documentchunk"
    ORDER BY content_embedded <=> :embedded_query_vector
    LIMIT :k
    """)

    query_result = await session.execute(
        query, {"embedded_query_vector": str(embedded_prompt_vector), "k": 5}
    )
    query_result = query_result.fetchall()

    # Adding search result to final prompt
    context = "\n".join(
        [
            f"Document{r.document_name}. Page {r.document_page_num}:\n{r.content_original}({r.document_chunk_index})"
            for r in query_result
        ]
    )

    final_prompt = f"""
    You are a helpful study assistant. Answer the question using ONLY the provided context.
    
    If the answer is not in the context, say "I don't know".
    
    Question:
    {prompt.question}
    
    Context:
    {context}
    
    Answer:
    """

    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt,
    )

    # UPDATE THIS LATER
    if response.text is None:
        raise

    return ModelResponse(answer=response.text)
