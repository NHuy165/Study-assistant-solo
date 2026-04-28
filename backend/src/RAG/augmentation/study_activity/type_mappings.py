from backend.src.models_schema.activity.json_validation import (
    FlashcardsJsonSchema,
    GapFillJsonSchema,
    MCQJsonSchema,
    OpenEndedJsonSchema,
    StudyActivityValidationBase,
)
from backend.src.models_schema.miscellaneous.enums import (
    StudyActivityFormat,
)
from backend.src.RAG.augmentation.study_activity.instruction_schemas import (
    flashcards_schema,
    gap_fill_schema,
    multiple_choice_questions_schema,
    open_ended_schema,
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
    StudyActivityFormat.GAP_FILL: (gap_fill_schema, GapFillJsonSchema),
    StudyActivityFormat.OPEN_ENDED: (open_ended_schema, OpenEndedJsonSchema),
}
