from abc import ABC, abstractmethod
from typing import Any

import ollama
from fastapi import UploadFile
from google import genai

from backend.src.core.config import settings
from backend.src.exceptions.core import ExceptionRequest_400

ai_client = genai.Client(api_key=settings.API_KEY_GEMINI)
ollama_client = ollama.AsyncClient(host=settings.OLLAMA_HOST)


class API(ABC):
    @classmethod
    @abstractmethod
    async def embed(cls, content: str) -> list[float]:
        """
        Embeds text into a 768-D vector.
        """
        pass

    @classmethod
    @abstractmethod
    async def describe_image(cls, file: UploadFile) -> str:
        """
        Generates a detailed description of the image.
        """
        pass

    @classmethod
    @abstractmethod
    async def generate_content(cls, prompt: str) -> str:
        """
        Generates an LLM response from a prompt.
        """
        pass


class GoogleAPI(API):
    @classmethod
    async def embed(cls, content: str) -> list[float]:
        response = await ai_client.aio.models.embed_content(
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
        response = await ai_client.aio.models.generate_content(
            model=settings.VISION_MODEL_GOOGLE,
            contents=[prompt_text, image_part],
        )

        # Validation
        if response.text is None:
            raise ExceptionRequest_400("Image could not be saved properly.")

        return response.text

    @classmethod
    async def generate_content(cls, prompt: str) -> str:
        response = await ai_client.aio.models.generate_content(
            model=settings.ANSWER_MODEL_GOOGLE,
            contents=prompt,
        )

        # Validation
        if response.text is None:
            raise ExceptionRequest_400(
                "A response could not be generated. Please recheck your question."
            )

        return response.text


class OllamaAPI(API):
    @classmethod
    async def embed(cls, content: str) -> list[float]:
        response = await ollama_client.embeddings(
            model=settings.EMBED_MODEL_OLLAMA,
            prompt=content,
        )

        embeddings = response.get("embedding")

        # Let this throw an internal error if wrong
        assert embeddings is not None
        assert isinstance(embeddings, list)

        if len(embeddings) > settings.DEFAULT_EMBED_DIMENSIONALITY:
            embeddings = embeddings[: settings.DEFAULT_EMBED_DIMENSIONALITY]

        return embeddings

    @classmethod
    async def describe_image(cls, file: UploadFile) -> str:
        # Extracting information from the image
        image_bytes = await file.read()

        prompt_text = "Extract all readable text from this image exactly as written.\nThen, describe the layout, charts, figures, subjects, and any data points in exhaustive detail."

        # Reads the image using the model
        response = await ollama_client.generate(
            model=settings.VISION_MODEL_OLLAMA,
            prompt=prompt_text,
            images=[image_bytes],
            options={"num_ctx": 8192},
        )

        result_text = response.get("response")

        # Validation
        if not result_text:
            raise ExceptionRequest_400("Image could not be saved properly.")

        return result_text

    @classmethod
    async def generate_content(cls, prompt: str) -> str:
        response = await ollama_client.generate(
            model=settings.ANSWER_MODEL_OLLAMA,
            prompt=prompt,
            options={"num_ctx": 8192},
        )

        result_text = response.get("response")

        # Validation
        if not result_text:
            raise ExceptionRequest_400(
                "A response could not be generated. Please recheck your question."
            )

        return result_text


class GlobalAPI(API):
    models: dict[str, type[API]] = {
        "GOOGLE": GoogleAPI,
        "OLLAMA": OllamaAPI,
    }

    @classmethod
    async def embed(cls, content: str) -> list[float]:
        return await cls.models[settings.MODEL_IN_USE].embed(content)

    @classmethod
    async def describe_image(cls, file: UploadFile) -> str:
        return await cls.models[settings.MODEL_IN_USE].describe_image(file)

    @classmethod
    async def generate_content(cls, prompt: str) -> str:
        return await cls.models[settings.MODEL_IN_USE].generate_content(prompt)
