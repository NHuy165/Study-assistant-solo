from enum import Enum


class DocumentType(str, Enum):
    PDF = "PDF"
    IMAGE = "IMAGE"
    TEXT = "TEXT"


class SubjectType(str, Enum):
    MATHS = "MATHS"
    ENGLISH = "ENGLISH"
    VIETNAMESE = "VIETNAMESE"


class StudyActivityType(str, Enum):
    REVIEW = "REVIEW"
    EXERCISE = "EXERCISE"


class StudyActivityFormat(str, Enum):
    # EXERCISE
    MULTIPLE_CHOICE_QUESTIONS = "MULTIPLE_CHOICE_QUESTIONS"
    OPEN_ENDED = "OPEN_ENDED"

    # REVIEW
    FLASHCARDS = "FLASHCARDS"
    TAP_TO_REVIEW = "TAP_TO_REVIEW"


class ReviewItemContentType(str, Enum):
    FLASHCARDS_FRONT = "FLASHCARDS_FRONT"
    FLASHCARDS_BACK = "FLASHCARDS_BACK"

    TAP_TO_REVIEW_TEXT = "TAP_TO_REVIEW_TEXT"
    TAP_TO_REVIEW_GAP = "TAP_TO_REVIEW_GAP"


class ExerciseItemContentType(str, Enum):
    MULTIPLE_CHOICE_QUESTIONS_CHOICE = "MULTIPLE_CHOICE_QUESTIONS_CHOICE"
