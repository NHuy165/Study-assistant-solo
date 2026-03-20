from sqlmodel import text

from backend.src.AI_services.utils import embed, process_pdf
from backend.src.core.config import ai_client
from backend.src.core.database import SessionDep
from backend.src.models_schema.document_chunk import DocumentChunk


async def save_chunks_service(session: SessionDep, file_name: str):
    chunks = process_pdf(file_name)

    for chunk in chunks:
        validated_model = DocumentChunk(**chunk)

        session.add(validated_model)
    await session.commit()


async def answer_query_service(session: SessionDep, query: str):
    embedded_query = embed(query).embeddings
    assert embedded_query is not None

    embedded_query_vector = embedded_query[0].values
    assert embedded_query_vector is not None

    search_query = text("""
    SELECT content_original, document_name, document_page_num, document_chunk_index
    FROM "documentchunk"
    ORDER BY content_embedded <=> :embedded_query_vector
    LIMIT :k
    """)

    result = await session.execute(
        search_query, {"embedded_query_vector": str(embedded_query_vector), "k": 5}
    )
    result = result.fetchall()

    context = "\n".join(
        [
            f"Document{r.document_name}. Page {r.document_page_num}:\n{r.content_original}({r.document_chunk_index})"
            for r in result
        ]
    )

    prompt = f"""
    You are a helpful study assistant. Answer the question using ONLY the provided context.
    
    If the answer is not in the context, say "I don't know".
    
    Question:
    {query}
    
    Context:
    {context}
    
    Answer:
    """

    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text
