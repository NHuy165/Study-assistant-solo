import asyncio
from datetime import date, datetime, timedelta, timezone
from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import Date, and_, cast, col, delete, func, or_, select
from sqlmodel.sql.expression import Select

from backend.src.core.ai_api import GlobalAPI
from backend.src.core.config import settings
from backend.src.core.dependencies import Interaction, User
from backend.src.exceptions.core import ExceptionNotFound_404
from backend.src.models_schema.activity.exercise_item import ExerciseItem
from backend.src.models_schema.activity.review_item import ReviewItem
from backend.src.models_schema.activity.study_activity import StudyActivity
from backend.src.models_schema.document.document import Document
from backend.src.models_schema.llm_response.llm_response import LLMResponse
from backend.src.models_schema.miscellaneous.enums import (
    AggregateTarget,
    CriterionAttribute,
    OperatorType,
    StudyActivityType,
    StudyAssessmentStatus,
)
from backend.src.models_schema.RAG.augmentation import StudyAssessmentParams
from backend.src.models_schema.study_progress.assessment import (
    MockStudyAssessmentInput,
    StudyAssessment,
)
from backend.src.models_schema.study_progress.criterion import Criterion
from backend.src.models_schema.user.check_in import CheckIn
from backend.src.RAG.augmentation.core.specific_augmentations import (
    study_assessment_augmentation,
)
from backend.src.RAG.augmentation.formatters.purpose_built.study_assessment import (
    progress_formatter,
)


async def mock_create_study_assessment(
    user: User,
    session: AsyncSession,
    current_datetime: datetime,
    mock_study_assessment_input: MockStudyAssessmentInput,
) -> StudyAssessment:
    study_assessment = StudyAssessment(
        assessment_of=mock_study_assessment_input.assessment_of,
        content=mock_study_assessment_input.content,
        user=user,
        created_at=current_datetime,
        status=StudyAssessmentStatus.COMPLETED,
    )

    session.add(study_assessment)
    await session.commit()

    return study_assessment
