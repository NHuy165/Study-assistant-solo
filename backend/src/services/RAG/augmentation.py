from backend.src.core.prompts import (
    ANSWER_GENERATION_BASE,
    STUDY_ACTIVITY_BASE,
)
from backend.src.models_schema.augmentation_params import (
    AnswerGenerationParams,
    AugmentationParams,
    StudyActivityParams,
)


def augmentation_generator(base: str, augmentation_params: type[AugmentationParams]):
    def augmentation(params: AugmentationParams) -> str:
        validated_params = augmentation_params.model_validate(params)
        final_prompt = base.format(**validated_params.model_dump(mode="json"))
        return final_prompt

    return augmentation


answer_generation_augmentation = augmentation_generator(
    ANSWER_GENERATION_BASE, AnswerGenerationParams
)
study_activity_augmentation = augmentation_generator(
    STUDY_ACTIVITY_BASE, StudyActivityParams
)
