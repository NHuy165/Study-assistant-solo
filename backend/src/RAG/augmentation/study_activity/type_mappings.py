from backend.src.models_schema.activity.json_validation import (
    FlashcardsJsonSchema,
    MCQJsonSchema,
    StudyActivityValidationBase,
    TapToReviewJsonSchema,
)
from backend.src.models_schema.miscellaneous.enums import (
    StudyActivityFormat,
)
from backend.src.RAG.augmentation.study_activity.instruction_schemas import (
    flashcards_schema,
    multiple_choice_questions_schema,
    tap_to_review_schema,
)

schema_map: dict[
    StudyActivityFormat | StudyActivityFormat,
    tuple[str, type[StudyActivityValidationBase]],
] = {
    StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS: (
        multiple_choice_questions_schema,
        MCQJsonSchema,
    ),
    StudyActivityFormat.FLASHCARDS: (flashcards_schema, FlashcardsJsonSchema),
    StudyActivityFormat.TAP_TO_REVIEW: (tap_to_review_schema, TapToReviewJsonSchema),
}
