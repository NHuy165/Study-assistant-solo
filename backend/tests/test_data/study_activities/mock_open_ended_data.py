from backend.src.core.config import settings

mock_open_ended_data = {
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

validation_open_ended_data = [
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
