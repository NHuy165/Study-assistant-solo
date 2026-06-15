from backend.src.core.config import settings

mock_MCQ_data = {
    "name": "Mock MCQ name",
    "description": "Mock MCQ description",
    "activity_items": [
        {
            "question": "Mock MCQ question 1",
            "answers": [
                "Mock MCQ answer 1-1",
                "Mock MCQ answer 1-2",
                "Mock MCQ answer 1-3",
                "Mock MCQ answer 1-4",
            ],
            "correct": 0,
        },
        {
            "question": "Mock MCQ question 2",
            "answers": [
                "Mock MCQ answer 2-1",
                "Mock MCQ answer 2-2",
                "Mock MCQ answer 2-3",
                "Mock MCQ answer 2-4",
            ],
            "correct": 1,
        },
        {
            "question": "Mock MCQ question 3",
            "answers": [
                "Mock MCQ answer 3-1",
                "Mock MCQ answer 3-2",
                "Mock MCQ answer 3-3",
                "Mock MCQ answer 3-4",
            ],
            "correct": 2,
        },
        {
            "question": "Mock MCQ question 4",
            "answers": [
                "Mock MCQ answer 4-1",
                "Mock MCQ answer 4-2",
                "Mock MCQ answer 4-3",
                "Mock MCQ answer 4-4",
            ],
            "correct": 3,
        },
        {
            "question": "Mock MCQ question 5",
            "answers": [
                "Mock MCQ answer 5-1",
                "Mock MCQ answer 5-2",
                "Mock MCQ answer 5-3",
                "Mock MCQ answer 5-4",
            ],
            "correct": 0,
        },
    ],
}

max_score = settings.DEFAULT_EXERCISE_TOTAL_SCORE / 5

validation_MCQ_data = [
    {
        "max_score": max_score,
        "question": "Mock MCQ question 1",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {
                "content": "Mock MCQ answer 1-1",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 1-2",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 1-3",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 1-4",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
        ],
    },
    {
        "max_score": max_score,
        "question": "Mock MCQ question 2",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {
                "content": "Mock MCQ answer 2-1",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 2-2",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 2-3",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 2-4",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
        ],
    },
    {
        "max_score": max_score,
        "question": "Mock MCQ question 3",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {
                "content": "Mock MCQ answer 3-1",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 3-2",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 3-3",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 3-4",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
        ],
    },
    {
        "max_score": max_score,
        "question": "Mock MCQ question 4",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {
                "content": "Mock MCQ answer 4-1",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 4-2",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 4-3",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 4-4",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
        ],
    },
    {
        "max_score": max_score,
        "question": "Mock MCQ question 5",
        "user_score": None,
        "explanation": None,
        "attempt": None,
        "contents": [
            {
                "content": "Mock MCQ answer 5-1",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 5-2",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 5-3",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
            {
                "content": "Mock MCQ answer 5-4",
                "type": "MULTIPLE_CHOICE_QUESTIONS_CHOICE",
                "is_correct": None,
            },
        ],
    },
]
