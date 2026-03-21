from pydantic import BaseModel


class ModelPrompt(BaseModel):
    question: str


class ModelResponse(BaseModel):
    answer: str
