from typing import Any

from pydantic import BaseModel

# ----- ACTIVITY ITEM SCHEMAS ----- #


class MCQSchema(BaseModel):
    question: str
    answers: list[str]
    correct: int


class FlashcardSchema(BaseModel):
    front: str
    back: str


class GapFillSchema(BaseModel):
    text: str
    correct: list[str]
    distractors: list[str]


class OpenEndedCreationSchema(BaseModel):
    question: str


class OpenEndedGradingInitiationSchema(BaseModel):
    id: int
    max_score: float
    question: str
    attempt: str | None


class OpenEndedGradingResultSchema(BaseModel):
    id: int
    user_score: float
    explanation: str


# ----- ACTIVITY BASE SCHEMAS  ----- #


class StudyActivityValidationBase(BaseModel):
    name: str
    description: str
    activity_items: list[Any]


# ----- SPECIFIC ACTIVITY SCHEMAS ----- #

# === Exercise === #


class MCQJsonSchema(StudyActivityValidationBase):
    activity_items: list[MCQSchema]


class OpenEndedCreationJsonSchema(StudyActivityValidationBase):
    activity_items: list[OpenEndedCreationSchema]


class OpenEndedGradingInitiationJsonSchema(BaseModel):
    questions_answers: list[OpenEndedGradingInitiationSchema]


class OpenEndedGradingResultJsonSchema(BaseModel):
    grading_results: list[OpenEndedGradingResultSchema]


# === Review === #


class FlashcardsJsonSchema(StudyActivityValidationBase):
    activity_items: list[FlashcardSchema]


class GapFillJsonSchema(StudyActivityValidationBase):
    activity_items: list[GapFillSchema]
