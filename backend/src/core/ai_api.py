import base64
from abc import ABC, abstractmethod
from typing import Any

import httpx
import ollama
from backend.src.core.config import settings
from backend.src.exceptions.core import ExceptionRequest_400
from fastapi import UploadFile
from google import genai

GOOGLE_CLIENT = genai.Client(api_key=settings.API_KEY_GEMINI)
OLLAMA_CLIENT = ollama.AsyncClient(host=settings.OLLAMA_HOST)

CLOUDFLARE_URL_EMBED = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/{settings.EMBED_MODEL_CLOUDFLARE}"
CLOUDFLARE_URL_IMAGE_CAPTION = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/{settings.VISION_MODEL_CLOUDFLARE}"
CLOUDFLARE_HEADERS = {
    "Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json",
}


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
    async def caption_image(cls, file: UploadFile) -> str:
        """
        Generates a detailed description of the image.
        """
        pass

    @classmethod
    @abstractmethod
    async def generate_content(cls, prompt: str, json_required: bool = False) -> str:
        """
        Generates an LLM response from a prompt.
        """
        pass


class GoogleAPI(API):
    @classmethod
    async def embed(cls, content: str) -> list[float]:
        response = await GOOGLE_CLIENT.aio.models.embed_content(
            model=settings.EMBED_MODEL_GOOGLE,
            contents=content,
            # Content is truncated from 3072-D to 768-D
            config=genai.types.EmbedContentConfig(
                output_dimensionality=settings.DEFAULT_EMBED_DIMENSIONALITY_GOOGLE_OLLAMA,
            ),
        )

        # Let this throw an internal error if wrong
        assert response.embeddings is not None
        assert isinstance(response.embeddings[0].values, list)

        return response.embeddings[0].values

    @classmethod
    async def caption_image(cls, file: UploadFile) -> str:
        # Extracting information from the image
        image_bytes = await file.read()

        prompt_text = "Extract all readable text from this image exactly as written.\nThen, describe the layout, charts, figures, subjects, and any data points in exhaustive detail."

        image_part = genai.types.Part.from_bytes(
            data=image_bytes,
            mime_type=file.content_type,  # type: ignore
        )

        # Reads the image using the model
        response = await GOOGLE_CLIENT.aio.models.generate_content(
            model=settings.VISION_MODEL_GOOGLE,
            contents=[prompt_text, image_part],
        )

        # Validation
        if response.text is None:
            raise ExceptionRequest_400("Image could not be saved properly.")

        return response.text

    @classmethod
    async def generate_content(cls, prompt: str, json_required: bool = False) -> str:
        config = genai.types.GenerateContentConfig()
        if json_required:
            config.response_mime_type = "application/json"

        response = await GOOGLE_CLIENT.aio.models.generate_content(
            model=settings.ANSWER_MODEL_GOOGLE,
            contents=prompt,
            config=config,
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
        response = await OLLAMA_CLIENT.embeddings(
            model=settings.EMBED_MODEL_OLLAMA,
            prompt=content,
        )

        embeddings = response.get("embedding")

        # Let this throw an internal error if wrong
        assert embeddings is not None
        assert isinstance(embeddings, list)

        if len(embeddings) > settings.DEFAULT_EMBED_DIMENSIONALITY_GOOGLE_OLLAMA:
            embeddings = embeddings[
                : settings.DEFAULT_EMBED_DIMENSIONALITY_GOOGLE_OLLAMA
            ]

        return embeddings

    @classmethod
    async def caption_image(cls, file: UploadFile) -> str:
        # Extracting information from the image
        image_bytes = await file.read()

        prompt_text = "Extract all readable text from this image exactly as written.\nThen, describe the layout, charts, figures, subjects, and any data points in exhaustive detail."

        # Reads the image using the model
        response = await OLLAMA_CLIENT.generate(
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
    async def generate_content(cls, prompt: str, json_required: bool = False) -> str:
        if json_required:
            response = await OLLAMA_CLIENT.generate(
                model=settings.ANSWER_MODEL_OLLAMA,
                prompt=prompt,
                options={"num_ctx": 8192},
                format="json",
            )
        else:
            response = await OLLAMA_CLIENT.generate(
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


class CloudFlareAPI(API):
    @classmethod
    async def embed(cls, content: str) -> list[float]:
        json_data = {"text": [content]}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                CLOUDFLARE_URL_EMBED, headers=CLOUDFLARE_HEADERS, json=json_data
            )

            assert response.status_code == 200

            response_data = response.json()

        assert response_data.get("result") is not None

        result_data = response_data.get("result", {}).get("data")

        assert result_data is not None
        assert isinstance(result_data, list)
        assert isinstance(result_data[0], list)

        return result_data[0]

    @classmethod
    async def caption_image(cls, file: UploadFile) -> str:
        # Cloudflare không còn trường image riêng biệt, giờ gửi ảnh thông qua json nên cần encode về chuỗi base64
        image_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        system_prompt = (
            "You are an expert AI vision assistant specialized in OCR, document transcription, "
            "and detailed visual analysis. Extract text exactly as written and describe layouts, "
            "data points, charts, and visual elements with exhaustive precision."
        )
        prompt_text = "Extract all readable text from this image exactly as written.\nThen, describe the layout, charts, figures, subjects, and any data points in exhaustive detail."

        json_data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text},
            ],
            "image": base64_image,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                CLOUDFLARE_URL_IMAGE_CAPTION, headers=CLOUDFLARE_HEADERS, json=json_data
            )

            response_data = response.json()

        if not response_data.get("success"):
            raise ExceptionRequest_400("Image could not be saved properly.")

        result_data = response_data.get("result", {}).get("response")

        assert result_data is not None
        assert isinstance(result_data, str)

        return result_data

    @classmethod
    async def generate_content(cls, prompt: str, json_required: bool = False) -> str:
        raise Exception("You weren't supposed to call this")


class GlobalAPI:
    models: dict[str, type[API]] = {
        "GOOGLE": GoogleAPI,
        "OLLAMA": OllamaAPI,
    }

    @classmethod
    async def embed(cls, content: str) -> list[float]:
        return await cls.models[settings.MODEL_IN_USE_EMBED].embed(content)

    @classmethod
    async def caption_image(cls, file: UploadFile) -> str:
        return await cls.models[settings.MODEL_IN_USE_CAPTION_IMAGE].caption_image(file)

    @classmethod
    async def generate_chat(cls, prompt: str) -> str:
        return await cls.models[settings.MODEL_IN_USE_GENERATE_CHAT].generate_content(
            prompt
        )

    @classmethod
    async def rewrite_prompt(cls, prompt: str) -> str:
        return await cls.models[settings.MODEL_IN_USE_REWRITE_PROMPT].generate_content(
            prompt
        )

    @classmethod
    async def generate_material(cls, prompt: str) -> str:
        return await cls.models[
            settings.MODEL_IN_USE_GENERATE_MATERIAL
        ].generate_content(prompt, json_required=True)

    @classmethod
    async def grade_answers(cls, prompt: str) -> str:
        return await cls.models[settings.MODEL_IN_USE_GRADE_ANSWERS].generate_content(
            prompt, json_required=True
        )
