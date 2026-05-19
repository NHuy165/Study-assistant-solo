from typing import Any

from pydantic import BaseModel

# ----- INDIVIDUAL ACTIVITY ITEM CREATION SCHEMAS ----- #


class MCQItemSchema(BaseModel):
    question: str
    answers: list[str]
    correct: int


class FlashcardItemSchema(BaseModel):
    front: str
    back: str


class GapFillItemSchema(BaseModel):
    text: str
    correct: list[str]
    distractors: list[str]


class OpenEndedItemSchema(BaseModel):
    question: str


# ----- INDIVIDUAL OPEN ENDED GRADING SCHEMAS ----- #


class OpenEndedGradingInitiationItemSchema(BaseModel):
    id: int
    max_score: float
    question: str
    attempt: str | None


class OpenEndedGradingResultItemSchema(BaseModel):
    id: int
    user_score: float
    explanation: str


# ----- ACTIVITY BASE SCHEMA ----- #


class StudyActivityValidationBase(BaseModel):
    name: str
    description: str
    activity_items: list[Any]


# ----- ACTIVITY CREATION SCHEMAS ----- #

# === Exercise === #


class MCQSchema(StudyActivityValidationBase):
    activity_items: list[MCQItemSchema]


class OpenEndedCreationSchema(StudyActivityValidationBase):
    activity_items: list[OpenEndedItemSchema]


# === Review === #


class FlashcardsSchema(StudyActivityValidationBase):
    activity_items: list[FlashcardItemSchema]


class GapFillSchema(StudyActivityValidationBase):
    activity_items: list[GapFillItemSchema]


# ----- OPEN ENDED GRADING SCHEMAS ----- #


class OpenEndedGradingInitiationSchema(BaseModel):
    questions_answers: list[OpenEndedGradingInitiationItemSchema]


class OpenEndedGradingResultSchema(BaseModel):
    grading_results: list[OpenEndedGradingResultItemSchema]
