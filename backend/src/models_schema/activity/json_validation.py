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


# ----- ACTIVITY BASE SCHEMAS  ----- #


class StudyActivityValidationBase(BaseModel):
    name: str
    description: str
    activity_items: list[Any]


# ----- SPECIFIC ACTIVITY SCHEMAS ----- #

# === Exercise === #


class MCQJsonSchema(StudyActivityValidationBase):
    activity_items: list[MCQSchema]


# === Review === #


class FlashcardsJsonSchema(StudyActivityValidationBase):
    activity_items: list[FlashcardSchema]
