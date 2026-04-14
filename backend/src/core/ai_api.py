from google import genai

from backend.src.core.config import settings

ai_client = genai.Client(api_key=settings.API_KEY_GEMINI)
