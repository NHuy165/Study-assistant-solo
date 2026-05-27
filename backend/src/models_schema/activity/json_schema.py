from typing import Any

from pydantic import BaseModel, model_validator

from backend.src.exceptions.core import ExceptionLLMError_502
from backend.src.models_schema.activity.study_activity import (
    OpenEndedGradingInitiationSchema,
)

# ----- INDIVIDUAL ACTIVITY ITEM CREATION SCHEMAS ----- #


class MCQItemSchema(BaseModel):
    question: str
    answers: list[str]
    correct: int

    @model_validator(mode="after")
    def validate_output(self):
        if len(self.answers) != 4 or self.correct not in (0, 1, 2, 3):
            raise ExceptionLLMError_502("Incorrect number of choices.")
        elif self.correct not in (0, 1, 2, 3):
            raise ExceptionLLMError_502("Incorrect correct answer indexing.")
        return self


class FlashcardItemSchema(BaseModel):
    front: str
    back: str


class GapFillItemSchema(BaseModel):
    text: str
    corrects: list[str]
    distractors: list[str]

    @model_validator(mode="after")
    def validate_output(self):
        blank_count = self.text.count("$!BLANK!$")
        if blank_count == 0:
            raise ExceptionLLMError_502("Text had no blank.")
        elif len(self.corrects) != blank_count:
            raise ExceptionLLMError_502(
                "The number of correct answers doesn't match the number of blanks."
            )
        return self


class OpenEndedItemSchema(BaseModel):
    question: str


# ----- INDIVIDUAL OPEN ENDED GRADING SCHEMAS ----- #


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


class OpenEndedGradingResultSchema(BaseModel):
    grading_input: OpenEndedGradingInitiationSchema
    grading_results: list[OpenEndedGradingResultItemSchema]

    @model_validator(mode="after")
    def validate_output(self):
        input_answers = {
            answer.id: answer.max_score
            for answer in self.grading_input.questions_answers
        }

        for grading_result in self.grading_results:
            max_score = input_answers.get(grading_result.id)
            if max_score is None:
                raise ExceptionLLMError_502("Incorrect graded answer id.")

            if grading_result.user_score < 0 or grading_result.user_score > max_score:
                raise ExceptionLLMError_502(
                    "Graded score fell outside of acceptable range."
                )

        return self
