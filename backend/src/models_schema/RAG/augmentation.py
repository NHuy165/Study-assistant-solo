from pydantic import BaseModel


class AugmentationParams(BaseModel):
    prompt: str


class AnswerGenerationParams(AugmentationParams):
    context_conversations: str
    context_document: str


class StudyActivityParams(AugmentationParams):
    context_conversations: str
    context_document: str
    subject_type: str
    json_schema: str
    study_activity_type: str


class PromptRewriteParams(AugmentationParams):
    context_conversations: str
