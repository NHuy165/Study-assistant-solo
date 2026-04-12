from pathlib import Path

from google import genai
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    # Private info
    POSTGRES_URL: PostgresDsn
    API_KEY_GEMINI: str
    PRIVATE_KEY: str

    # Technical config

    # Auth
    JWT_ALGORITHM: str
    TOKEN_EXPIRY_HOURS: int

    # Models
    EMBED_MODEL: str
    ANSWER_MODEL: str

    # RAG
    DEFAULT_CHUNK_SIZE: int
    DEFAULT_CHUNK_OVERLAP: int
    N_CHUNKS_RETRIEVED: int
    N_PAST_CONVERSATIONS: int

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )


settings = Settings()  # type: ignore

ai_client = genai.Client(api_key=settings.API_KEY_GEMINI)
