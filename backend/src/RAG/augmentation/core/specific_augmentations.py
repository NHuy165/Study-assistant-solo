from backend.src.models_schema.RAG.augmentation import (
    AnswerGenerationParams,
    AugmentationParams,
    StudyActivityParams,
)
from backend.src.RAG.augmentation.chunk_rewriting.rewrite import PromptRewriteParams
from backend.src.RAG.augmentation.core.base_prompts import (
    ANSWER_GENERATION_BASE,
    PROMPT_REWRITE_BASE,
    STUDY_ACTIVITY_BASE,
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
prompt_rewrite_augmentation = augmentation_generator(
    PROMPT_REWRITE_BASE, PromptRewriteParams
)
