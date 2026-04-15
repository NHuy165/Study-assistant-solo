from backend.src.core.ai_api import GlobalAPI

PROMPT_REWRITE_BASE = """=== ROLE & OBJECTIVE ===
You are an expert Database Query Optimizer. 
The user is a Vietnamese primary school student (Grades 1-5), seeking knowledge in the 3 subjects: literature, maths and english.
Your task is to read the student's current raw input AND the conversation history, then rewrite their input into a concise, highly accurate academic search query to be used in a Vector Database (textbook retrieval).

=== STRICT RULES ===
1. OUTPUT FORMAT: You must output ONLY the rewritten search query. No explanations, no pleasantries, do not answer the question. Try your best to keep the main idea of the initial query and do not make assumptions about the user's intent.
2. TARGET LANGUAGE: The core query must be in Vietnamese. HOWEVER, if the question is about the English subject (e.g., vocabulary, grammar), you MUST keep the relevant English words exactly as they are so they can match the English textbook.
3. PRESERVE METADATA: You MUST explicitly keep any page numbers, unit names, lesson numbers, or specific textbook mentions... (e.g., "trang 5", "bài 2", "toán lớp 3"). Never remove these details.
4. FIX & ENHANCE: Correct any Vietnamese spelling or grammar mistakes from the student. Expand kid-friendly terms into academic textbook terms (e.g., "cộng" -> "phép cộng").
5. CONTEXT RESOLUTION: If the student uses pronouns (it, that, this) or refers to previous steps, look at the PAST CONVERSATIONS and replace those pronouns with the exact specific nouns they represent. This step is to prevent context loss, as the past conversations will not be used in the vector search.

=== PAST CONVERSATIONS ===
{context_conversations}

=== CURRENT RAW PROMPT ===
{raw_prompt}

=== OPTIMIZED SEARCH QUERY ===
"""


async def rewrite_prompt(raw_prompt: str, context_conversations: str) -> str:
    prompt_rewrite = PROMPT_REWRITE_BASE.format(
        context_conversations=context_conversations, raw_prompt=raw_prompt
    )

    rewritten_prompt = await GlobalAPI.generate_content(prompt_rewrite)

    return rewritten_prompt
