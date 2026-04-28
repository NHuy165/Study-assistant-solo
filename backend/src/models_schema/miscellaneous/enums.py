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
    GAP_FILL = "GAP_FILL"


class ReviewItemContentType(str, Enum):
    FLASHCARDS_FRONT = "FLASHCARDS_FRONT"
    FLASHCARDS_BACK = "FLASHCARDS_BACK"

    GAP_FILL_TEXT = "GAP_FILL_TEXT"
    GAP_FILL_CORRECT = "GAP_FILL_CORRECT"
    GAP_FILL_DISTRACTOR = "GAP_FILL_DISTRACTOR"


class ExerciseItemContentType(str, Enum):
    MULTIPLE_CHOICE_QUESTIONS_CHOICE = "MULTIPLE_CHOICE_QUESTIONS_CHOICE"
