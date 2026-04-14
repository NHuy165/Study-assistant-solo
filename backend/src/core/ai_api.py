from abc import ABC, abstractmethod
from typing import Any

from fastapi import UploadFile
from google import genai

from backend.src.core.config import settings
from backend.src.exceptions.core import ExceptionRequest_400

ai_client = genai.Client(api_key=settings.API_KEY_GEMINI)


class API(ABC):
    @classmethod
    @abstractmethod
    def embed(cls, content: str) -> list[float]:
        """
        Embeds text into a 768-D vector.
        """
        pass

    @classmethod
    @abstractmethod
    def describe_image(cls, file: UploadFile) -> str:
        """
        Generates a detailed description of the image.
        """
        pass

    @classmethod
    @abstractmethod
    def generate_content(cls, prompt: str) -> str:
        """
        Generates an LLM response from a prompt.
        """
        pass


class GoogleAPI(API):
    @classmethod
    def embed(cls, content: str) -> list[float]:
        response = ai_client.models.embed_content(
            model=settings.EMBED_MODEL_GOOGLE,
            contents=content,
            # Content is truncated from 3072-D to 768-D
            config=genai.types.EmbedContentConfig(
                output_dimensionality=settings.DEFAULT_EMBED_DIMENSIONALITY,
            ),
        )

        # Let this throw an internal error if wrong
        assert response.embeddings is not None
        assert isinstance(response.embeddings[0].values, list)

        return response.embeddings[0].values

    @classmethod
    async def describe_image(cls, file: UploadFile) -> str:
        # Extracting information from the image
        image_bytes = await file.read()

        prompt_text = "Extract all readable text from this image exactly as written.\nThen, describe the layout, charts, figures, subjects, and any data points in exhaustive detail."

        image_part = genai.types.Part.from_bytes(
            data=image_bytes,
            mime_type=file.content_type,  # type: ignore
        )

        # Reads the image using the model
        response = ai_client.models.generate_content(
            model=settings.VISION_MODEL_GOOGLE,
            contents=[prompt_text, image_part],
        )

        # Validation
        if response.text is None:
            raise ExceptionRequest_400("Image could not be saved properly.")

        return response.text

    @classmethod
    def generate_content(cls, prompt: str) -> str:
        response = ai_client.models.generate_content(
            model=settings.ANSWER_MODEL_GOOGLE,
            contents=prompt,
        )

        # Validation
        if response.text is None:
            raise ExceptionRequest_400(
                "A response could not be generated. Please recheck your question."
            )

        return response.text
