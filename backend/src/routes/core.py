import google.generativeai as genai
from fastapi import APIRouter, HTTPException

from backend.src.core.config import settings
from backend.src.models_schema.user_query import UserQuery

router = APIRouter()

base_knowledge = """
The P2P Marketplace platform charges a 5% transaction fee on all successful trades.
Users must verify their email before they can post an item.
"""

pretext = f"""
You are a helpful assistant for a P2P marketplace.
Answer the user's question using ONLY the following context:

Context:
{base_knowledge}
"""

genai.configure(api_key=settings.API_KEY_GEMINI)

model = genai.GenerativeModel("gemini-2.5-flash")


@router.post("/ask")
async def ask(query: UserQuery):
    try:
        augmented_prompt = f"""
        {pretext}

        User question: {query.question}
        """

        response = await model.generate_content_async(augmented_prompt)

        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
