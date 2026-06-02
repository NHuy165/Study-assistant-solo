from typing import Callable

<<<<<<< HEAD
from pydantic import BaseModel

from backend.src.models_schema.RAG.augmentation import (
    AnswerGenerationParams,
    AugmentationParams,
    DocumentAnalysisParams,
=======
from backend.src.models_schema.RAG.augmentation import (
    AnswerGenerationParams,
    AugmentationParams,
>>>>>>> 1265ccb (feat(BE): Thêm tính năng giải thích khi nộp bài tập trắc nghiệm. Ngoài ra chỉnh sửa lại vài chỗ ở các prompt nộp bài cũ.)
    GradingParams,
    PromptRewriteParams,
    StudyActivityParams,
    StudyAssessmentParams,
)
from backend.src.RAG.augmentation.prompts_formatting.base_prompts import (
<<<<<<< HEAD
    ANSWER_GENERATION_BASE_PROMPT,
    DOCUMENT_ANALYSIS_BASE_PROMPT,
    MCQ_GRADING_BASE_PROMPT,
    OPEN_ENDED_GRADING_BASE_PROMPT,
    PROMPT_REWRITE_BASE_PROMPT,
    STUDY_ACTIVITY_BASE_PROMPT,
    STUDY_ASSESSMENT_BASE_PROMPT,
=======
    ANSWER_GENERATION_BASE,
    MCQ_GRADING_BASE,
    OPEN_ENDED_GRADING_BASE,
    PROMPT_REWRITE_BASE,
    STUDY_ACTIVITY_BASE,
>>>>>>> 1265ccb (feat(BE): Thêm tính năng giải thích khi nộp bài tập trắc nghiệm. Ngoài ra chỉnh sửa lại vài chỗ ở các prompt nộp bài cũ.)
)


def augmentation_generator(
<<<<<<< HEAD
    base_prompt: str, augmentation_params: type[BaseModel]
) -> Callable[[BaseModel], str]:
    def augmentation(params: BaseModel) -> str:
=======
    base: str, augmentation_params: type[AugmentationParams]
) -> Callable[[AugmentationParams], str]:
    def augmentation(params: AugmentationParams) -> str:
>>>>>>> 1265ccb (feat(BE): Thêm tính năng giải thích khi nộp bài tập trắc nghiệm. Ngoài ra chỉnh sửa lại vài chỗ ở các prompt nộp bài cũ.)
        validated_params = augmentation_params.model_validate(params)
        final_prompt = base_prompt.format(**validated_params.model_dump(mode="json"))
        return final_prompt

    return augmentation


answer_generation_augmentation = augmentation_generator(
<<<<<<< HEAD
    ANSWER_GENERATION_BASE_PROMPT,
    AnswerGenerationParams,
)
study_activity_augmentation = augmentation_generator(
    STUDY_ACTIVITY_BASE_PROMPT,
    StudyActivityParams,
)
prompt_rewrite_augmentation = augmentation_generator(
    PROMPT_REWRITE_BASE_PROMPT,
    PromptRewriteParams,
)
open_ended_grading_augmentation = augmentation_generator(
    OPEN_ENDED_GRADING_BASE_PROMPT,
    GradingParams,
)
mcq_grading_augmentation = augmentation_generator(
    MCQ_GRADING_BASE_PROMPT,
    GradingParams,
)
document_analysis_augmentation = augmentation_generator(
    DOCUMENT_ANALYSIS_BASE_PROMPT,
    DocumentAnalysisParams,
)
study_assessment_augmentation = augmentation_generator(
    STUDY_ASSESSMENT_BASE_PROMPT,
    StudyAssessmentParams,
=======
    ANSWER_GENERATION_BASE,
    AnswerGenerationParams,
)
study_activity_augmentation = augmentation_generator(
    STUDY_ACTIVITY_BASE,
    StudyActivityParams,
)
prompt_rewrite_augmentation = augmentation_generator(
    PROMPT_REWRITE_BASE,
    PromptRewriteParams,
)
open_ended_grading_augmentation = augmentation_generator(
    OPEN_ENDED_GRADING_BASE,
    GradingParams,
)
mcq_grading_augmentation = augmentation_generator(
    MCQ_GRADING_BASE,
    GradingParams,
>>>>>>> 1265ccb (feat(BE): Thêm tính năng giải thích khi nộp bài tập trắc nghiệm. Ngoài ra chỉnh sửa lại vài chỗ ở các prompt nộp bài cũ.)
)
