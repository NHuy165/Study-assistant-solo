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


class ExerciseActivityType(str, Enum):
    MCQ = "MULTIPLE_CHOICE_QUESTIONS"
    OPEN_ENDED = "OPEN_ENDED"


class ReviewActivityType(str, Enum):
    FLASHCARDS = "FLASHCARDS"
    MINDMAP = "MINDMAP"
