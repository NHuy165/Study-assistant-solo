from backend.src.models_schema.miscellaneous.enums import (
    ReviewItemContentType,
    StudyActivityFormat,
    StudyActivityType,
)

mock_flashcards_llm_return_data = {
    "name": "Mock flashcards name",
    "description": "Mock flashcards description",
    "activity_items": [
        {
            "front": "Mock front 1",
            "back": "Mock back 1",
        },
        {
            "front": "Mock front 2",
            "back": "Mock back 2",
        },
        {
            "front": "Mock front 3",
            "back": "Mock back 3",
        },
        {
            "front": "Mock front 4",
            "back": "Mock back 4",
        },
        {
            "front": "Mock front 5",
            "back": "Mock back 5",
        },
    ],
}

validation_flashcards_creation_data = [
    {
        "contents": [
            {
                "content": "Mock front 1",
                "type": "FLASHCARDS_FRONT",
            },
            {
                "content": "Mock back 1",
                "type": "FLASHCARDS_BACK",
            },
        ]
    },
    {
        "contents": [
            {
                "content": "Mock front 2",
                "type": "FLASHCARDS_FRONT",
            },
            {
                "content": "Mock back 2",
                "type": "FLASHCARDS_BACK",
            },
        ]
    },
    {
        "contents": [
            {
                "content": "Mock front 3",
                "type": "FLASHCARDS_FRONT",
            },
            {
                "content": "Mock back 3",
                "type": "FLASHCARDS_BACK",
            },
        ]
    },
    {
        "contents": [
            {
                "content": "Mock front 4",
                "type": "FLASHCARDS_FRONT",
            },
            {
                "content": "Mock back 4",
                "type": "FLASHCARDS_BACK",
            },
        ]
    },
    {
        "contents": [
            {
                "content": "Mock front 5",
                "type": "FLASHCARDS_FRONT",
            },
            {
                "content": "Mock back 5",
                "type": "FLASHCARDS_BACK",
            },
        ]
    },
]

validation_flashcards_read_data = {
    "activity_type": StudyActivityType.REVIEW,
    "activity_format": StudyActivityFormat.FLASHCARDS,
    "is_submitted": False,
    "items": [
        {
            "contents": [
                {
                    "content": "Flashcard front 1",
                    "type": ReviewItemContentType.FLASHCARDS_FRONT,
                },
                {
                    "content": "Flashcard back 1",
                    "type": ReviewItemContentType.FLASHCARDS_BACK,
                },
            ],
        },
        {
            "contents": [
                {
                    "content": "Flashcard front 2",
                    "type": ReviewItemContentType.FLASHCARDS_FRONT,
                },
                {
                    "content": "Flashcard back 2",
                    "type": ReviewItemContentType.FLASHCARDS_BACK,
                },
            ],
        },
    ],
}
