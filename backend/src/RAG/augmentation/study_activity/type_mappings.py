from backend.src.models_schema.activity.json_validation import (
    FlashcardsJsonSchema,
    MCQJsonSchema,
    StudyActivityValidationBase,
)
from backend.src.models_schema.miscellaneous.enums import (
    ExerciseActivityType,
    ReviewActivityType,
)
from backend.src.RAG.augmentation.study_activity.instructions import (
    flashcard_schema,
    mcq_schema,
)

schema_map: dict[
    ExerciseActivityType | ReviewActivityType,
    tuple[str, type[StudyActivityValidationBase]],
] = {
    ExerciseActivityType.MCQ: (mcq_schema, MCQJsonSchema),
    ReviewActivityType.FLASHCARDS: (flashcard_schema, FlashcardsJsonSchema),
}
