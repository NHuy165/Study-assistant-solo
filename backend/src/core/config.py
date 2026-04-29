from pathlib import Path

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
    MODEL_IN_USE_EMBED: str
    MODEL_IN_USE_CAPTION_IMAGE: str
    MODEL_IN_USE_GENERATE_CHAT: str
    MODEL_IN_USE_REWRITE_PROMPT: str
    MODEL_IN_USE_GENERATE_MATERIAL: str
    MODEL_IN_USE_GRADE_ANSWERS: str

    EMBED_MODEL_GOOGLE: str
    VISION_MODEL_GOOGLE: str
    ANSWER_MODEL_GOOGLE: str

    OLLAMA_HOST: str
    EMBED_MODEL_OLLAMA: str
    VISION_MODEL_OLLAMA: str
    ANSWER_MODEL_OLLAMA: str

    # RAG
    DEFAULT_CHUNK_SIZE: int
    DEFAULT_CHUNK_OVERLAP: int
    DEFAULT_EMBED_DIMENSIONALITY: int
    N_CHUNKS_RETRIEVED: int
    N_PAST_CONVERSATIONS: int
    N_CHUNKS_WINDOW: int

    # STUDY ACTIVITY
    DEFAULT_EXERCISE_TOTAL_SCORE: float

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )


settings = Settings()  # type: ignore
