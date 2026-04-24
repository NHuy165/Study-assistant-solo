from backend.src.models_schema.activity.json_validation import (
    FlashcardsJsonSchema,
    MCQJsonSchema,
    StudyActivityValidationBase,
)
from backend.src.models_schema.miscellaneous.enums import (
    StudyActivityFormat,
)
from backend.src.RAG.augmentation.study_activity.instruction_schemas import (
    flashcard_schema,
    mcq_schema,
)

schema_map: dict[
    StudyActivityFormat | StudyActivityFormat,
    tuple[str, type[StudyActivityValidationBase]],
] = {
    StudyActivityFormat.MULTIPLE_CHOICE_QUESTIONS: (mcq_schema, MCQJsonSchema),
    StudyActivityFormat.FLASHCARDS: (flashcard_schema, FlashcardsJsonSchema),
}
