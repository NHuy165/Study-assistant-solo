from backend.src.models_schema.activity.activity_schemas import (
    FlashcardsJsonSchema,
    MCQJsonSchema,
    StudyActivityValidationBase,
)
from backend.src.models_schema.enums import ExerciseActivityType, ReviewActivityType
from backend.src.services.RAG.activity_schemas_instructions import (
    flashcard_schema,
    mcq_schema,
)

schema_map: dict[
    ExerciseActivityType | ReviewActivityType,
    tuple[str, type[StudyActivityValidationBase]],
] = {
    # ExerciseActivityType
    ExerciseActivityType.MCQ: (mcq_schema, MCQJsonSchema),
    ReviewActivityType.FLASHCARDS: (flashcard_schema, FlashcardsJsonSchema),
}
