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


class ExerciseActivityValidationBase(StudyActivityValidationBase):
    questions: list[Any]


class ReviewActivityValidationBase(StudyActivityValidationBase):
    contents: list[Any]


# ----- SPECIFIC ACTIVITY SCHEMAS ----- #

# === Exercise === #


class MCQJsonSchema(ExerciseActivityValidationBase):
    questions: list[MCQSchema]


# === Review === #


class FlashcardsJsonSchema(ReviewActivityValidationBase):
    contents: list[FlashcardSchema]
