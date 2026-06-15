mock_gap_fill_data = {
    "name": "Mock gap fill name",
    "description": "Mock gap fill description",
    "activity_items": [
        {
            "text": "Mock: $!BLANK!$",
            "corrects": ["Mock correct answer 1-1"],
            "distractors": ["Mock distractor 1-1"],
        },
        {
            "text": "Mock: $!BLANK!$ $!BLANK!$",
            "corrects": ["Mock correct answer 2-1", "Mock correct answer 2-2"],
            "distractors": ["Mock distractor 2-1", "Mock distractor 2-2"],
        },
        {
            "text": "Mock: $!BLANK!$ $!BLANK!$ $!BLANK!$",
            "corrects": [
                "Mock correct answer 3-1",
                "Mock correct answer 3-2",
                "Mock correct answer 3-3",
            ],
            "distractors": [
                "Mock distractor 3-1",
                "Mock distractor 3-2",
                "Mock distractor 3-3",
            ],
        },
        {
            "text": "Mock: $!BLANK!$ $!BLANK!$ $!BLANK!$ $!BLANK!$",
            "corrects": [
                "Mock correct answer 4-1",
                "Mock correct answer 4-2",
                "Mock correct answer 4-3",
                "Mock correct answer 4-4",
            ],
            "distractors": [
                "Mock distractor 4-1",
                "Mock distractor 4-2",
                "Mock distractor 4-3",
                "Mock distractor 4-4",
            ],
        },
        {
            "text": "Mock: $!BLANK!$ $!BLANK!$ $!BLANK!$ $!BLANK!$ $!BLANK!$",
            "corrects": [
                "Mock correct answer 5-1",
                "Mock correct answer 5-2",
                "Mock correct answer 5-3",
                "Mock correct answer 5-4",
                "Mock correct answer 5-5",
            ],
            "distractors": [
                "Mock distractor 5-1",
                "Mock distractor 5-2",
                "Mock distractor 5-3",
                "Mock distractor 5-4",
                "Mock distractor 5-5",
            ],
        },
    ],
}

validation_gap_fill_data = [
    {
        "contents": [
            {
                "content": "Mock: $!BLANK!$",
                "type": "GAP_FILL_TEXT",
            },
            {
                "content": "Mock correct answer 1-1",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock distractor 1-1",
                "type": "GAP_FILL_DISTRACTOR",
            },
        ],
    },
    {
        "contents": [
            {
                "content": "Mock: $!BLANK!$ $!BLANK!$",
                "type": "GAP_FILL_TEXT",
            },
            {
                "content": "Mock correct answer 2-1",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 2-2",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock distractor 2-1",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 2-2",
                "type": "GAP_FILL_DISTRACTOR",
            },
        ],
    },
    {
        "contents": [
            {
                "content": "Mock: $!BLANK!$ $!BLANK!$ $!BLANK!$",
                "type": "GAP_FILL_TEXT",
            },
            {
                "content": "Mock correct answer 3-1",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 3-2",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 3-3",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock distractor 3-1",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 3-2",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 3-3",
                "type": "GAP_FILL_DISTRACTOR",
            },
        ],
    },
    {
        "contents": [
            {
                "content": "Mock: $!BLANK!$ $!BLANK!$ $!BLANK!$ $!BLANK!$",
                "type": "GAP_FILL_TEXT",
            },
            {
                "content": "Mock correct answer 4-1",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 4-2",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 4-3",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 4-4",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock distractor 4-1",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 4-2",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 4-3",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 4-4",
                "type": "GAP_FILL_DISTRACTOR",
            },
        ],
    },
    {
        "contents": [
            {
                "content": "Mock: $!BLANK!$ $!BLANK!$ $!BLANK!$ $!BLANK!$ $!BLANK!$",
                "type": "GAP_FILL_TEXT",
            },
            {
                "content": "Mock correct answer 5-1",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 5-2",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 5-3",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 5-4",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock correct answer 5-5",
                "type": "GAP_FILL_CORRECT",
            },
            {
                "content": "Mock distractor 5-1",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 5-2",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 5-3",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 5-4",
                "type": "GAP_FILL_DISTRACTOR",
            },
            {
                "content": "Mock distractor 5-5",
                "type": "GAP_FILL_DISTRACTOR",
            },
        ],
    },
]
