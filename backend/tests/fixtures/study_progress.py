from datetime import date, datetime, timezone
from types import CoroutineType
from typing import Any, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models_schema.miscellaneous.enums import StudyAssessmentStatus
from backend.src.models_schema.study_progress.assessment import StudyAssessment
from backend.src.models_schema.user.user import User


@pytest.fixture(name="create_study_assessment_custom")
async def create_study_assessment_custom_fixture(
    session: AsyncSession,
) -> Callable[[User, date, datetime | None], CoroutineType[Any, Any, StudyAssessment]]:
    """
    Returns a function that creates a study assessment from a certain date.
    """

    async def create_study_assessment_custom(
        user: User,
        date: date,
        created_at: datetime | None,
    ) -> StudyAssessment:

        study_assessment = StudyAssessment(
            assessment_of=date,
            content=f"Study assessment of {date.isoformat()}",
            created_at=created_at if created_at else datetime.now(timezone.utc),
            user=user,
            status=StudyAssessmentStatus.COMPLETED,
        )

        session.add(study_assessment)
        await session.commit()

        return study_assessment

    return create_study_assessment_custom
