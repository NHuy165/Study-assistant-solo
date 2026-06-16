from backend.src.core.config import settings
from backend.src.models_schema.miscellaneous.enums import (
    ExerciseItemContentType,
    StudyActivityFormat,
    StudyActivityType,
)

mock_open_ended_llm_return_data = {
    "name": "Mock open ended name",
    "description": "Mock open ended description",
    "activity_items": [
        {
            "question": "Mock question 1",
            "correct": "Mock correct answer 1",
        },
        {
            "question": "Mock question 2",
            "correct": "Mock correct answer 2",
        },
        {
            "question": "Mock question 3",
            "correct": "Mock correct answer 3",
        },
        {
            "question": "Mock question 4",
            "correct": "Mock correct answer 4",
        },
        {
            "question": "Mock question 5",
            "correct": "Mock correct answer 5",
        },
    ],
}

max_score = settings.DEFAULT_EXERCISE_TOTAL_SCORE / 5

validation_open_ended_creation_data = [
    {
        "max_score": max_score,
        "question": "Mock question 1",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {"content": None, "type": "OPEN_ENDED_CORRECT", "is_correct": True}
        ],
    },
    {
        "max_score": max_score,
        "question": "Mock question 2",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {"content": None, "type": "OPEN_ENDED_CORRECT", "is_correct": True}
        ],
    },
    {
        "max_score": max_score,
        "question": "Mock question 3",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {"content": None, "type": "OPEN_ENDED_CORRECT", "is_correct": True}
        ],
    },
    {
        "max_score": max_score,
        "question": "Mock question 4",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {"content": None, "type": "OPEN_ENDED_CORRECT", "is_correct": True}
        ],
    },
    {
        "max_score": max_score,
        "question": "Mock question 5",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {"content": None, "type": "OPEN_ENDED_CORRECT", "is_correct": True}
        ],
    },
]

validation_open_ended_read_data = {
    "activity_type": StudyActivityType.EXERCISE,
    "activity_format": StudyActivityFormat.OPEN_ENDED,
    "is_submitted": True,
    "items": [
        {
            "question": "Question 1",
            "user_score": 50,
            "attempt": "Answer 1",
            "contents": [
                {
                    "content": "Correct answer 1",
                    "type": ExerciseItemContentType.OPEN_ENDED_CORRECT,
                    "is_correct": True,
                },
            ],
        },
        {
            "question": "Question 2",
            "user_score": 0,
            "attempt": None,
            "contents": [
                {
                    "content": "Correct answer 2",
                    "type": ExerciseItemContentType.OPEN_ENDED_CORRECT,
                    "is_correct": True,
                },
            ],
        },
    ],
}
