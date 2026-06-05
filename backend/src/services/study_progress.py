<<<<<<< HEAD
import asyncio
from datetime import date, datetime, timezone
from tabnanny import check
=======
from datetime import date, datetime, timezone
>>>>>>> f8fd44f (feat(BE): Cho phép developers nhập ngày giả vào trong endpoint để test.)
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import Date, and_, cast, col, func, or_, select
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
)
from backend.src.models_schema.RAG.augmentation import StudyAssessmentParams
from backend.src.models_schema.study_progress.assessment import StudyAssessment
from backend.src.models_schema.study_progress.criterion import Criterion
from backend.src.models_schema.user.check_in import CheckIn
from backend.src.RAG.augmentation.core.specific_augmentations import (
    study_assessment_augmentation,
)
from backend.src.RAG.augmentation.formatters.purpose_built.study_assessment import (
    progress_formatter,
)

# ----- CREATE ----- #


async def create_study_assessment_prompt(user: User, session, day: date) -> str:
    # === Fetches data === #

    # Fetches documents
    query_fetched_documents = (
        select(Document)
        .join(Interaction)
        .where(
            Interaction.user_id == user.id,
            func.cast(Document.created_at, Date) == day,  # type: ignore
        )
        .order_by(col(Document.created_at).desc())
        .limit(settings.DEFAULT_N_DOCUMENTS_FETCHED)
        .options(selectinload(Document.document_analysis))  # type: ignore
    )
    fetched_documents = (await session.execute(query_fetched_documents)).scalars().all()

    # Fetches LLM responses
    query_fetched_llm_responses = (
        select(LLMResponse)
        .join(Interaction)
        .where(
            Interaction.user_id == user.id,
            func.cast(col(LLMResponse.created_at), Date) == day,
        )
        .order_by(col(LLMResponse.created_at).desc())
        .limit(settings.DEFAULT_N_LLM_RESPONSES_FETCHED)
    )
    fetched_llm_responses = (
        (await session.execute(query_fetched_llm_responses)).scalars().all()
    )
    # formatted_llm_responses = conversations_formatter(fetched_llm_responses)

    # Fetches study activities
    query_fetched_study_activities = (
        select(StudyActivity)
        .join(Interaction)
        .where(
            Interaction.user_id == user.id,
            func.cast(col(StudyActivity.created_at), Date) == day,
            or_(
                StudyActivity.activity_type == StudyActivityType.REVIEW,
                and_(
                    StudyActivity.activity_type == StudyActivityType.EXERCISE,
                    or_(
                        StudyActivity.is_submitted == True,
                        StudyActivity.is_deleted == False,
                    ),
                ),
            ),
        )
        .order_by(col(StudyActivity.created_at).desc())
        .limit(settings.DEFAULT_N_STUDY_ACTIVITIES_FETCHED)
        .options(
            selectinload(
                StudyActivity.review_items.and_(ReviewItem.is_deleted == False)  # type: ignore
            ).selectinload(ReviewItem.contents),  # type: ignore
            selectinload(
                StudyActivity.exercise_items.and_(ExerciseItem.is_deleted == False)  # type: ignore
            ).selectinload(
                ExerciseItem.contents  # type: ignore
            ),
        )
    )
    fetched_study_activities = (
        (await session.execute(query_fetched_study_activities)).scalars().all()
    )

    # === Augmentation === #
    all_events = (
        list(fetched_documents)
        + list(fetched_llm_responses)
        + list(fetched_study_activities)
    )
    all_events.sort(key=lambda event: event.created_at)
    formatted_events = progress_formatter(all_events)

    params = StudyAssessmentParams(
        personal_information=user.description,
        context_events=formatted_events,
    )
    final_prompt = study_assessment_augmentation(params)

    return final_prompt


async def create_study_assessment(
    user: User, session: AsyncSession, day_overwrite: date | None
) -> StudyAssessment | None:
    today = day_overwrite if day_overwrite else datetime.now(timezone.utc).date()

    # Checks check ins without assessment
    query_last_check_in = (
        select(CheckIn)
        .outerjoin(
            StudyAssessment,
            col(CheckIn.time) == col(StudyAssessment.assessment_of),
        )
        .where(
            CheckIn.user_id == user.id,
            CheckIn.time < today,
            col(StudyAssessment.id).is_(None),
        )
        .order_by(col(CheckIn.time).desc())
    )
    check_ins_without_assessment = (
        (await session.execute(query_last_check_in)).scalars().all()
    )

    # Creates assessments
    final_prompts = [
        await create_study_assessment_prompt(user, session, check_in.time)
        for check_in in check_ins_without_assessment
    ]

    assessment_tasks = [
        GlobalAPI.generate_study_assessment(final_prompt)
        for final_prompt in final_prompts
    ]

    study_assessment_texts = await asyncio.gather(*assessment_tasks)

    study_assessments = [
        StudyAssessment(assessment_of=check_in.time, content=text, user=user)  # type: ignore
        for check_in, text in zip(check_ins_without_assessment, study_assessment_texts)
    ]

    session.add_all(study_assessments)
    await session.commit()

    return study_assessments[0] if study_assessments else None


# ----- READ ----- #


def process_group_bys(criteria: list[Criterion]) -> list[Any]:
    i = 0
    group_cols = []

    while i < len(criteria):
        if criteria[i].operator == OperatorType.GROUP_BY:
            criterion = criteria.pop(i)

            if criterion.attribute in (
                CriterionAttribute.CREATED_AT,
                CriterionAttribute.SUBMITTED_AT,
            ):
                raw_col = col(getattr(StudyActivity, criterion.attribute.value))
                utc_col = func.timezone("UTC", raw_col)
                group_cols.append(cast(utc_col, Date))
            else:
                group_cols.append(
                    col(getattr(StudyActivity, criterion.attribute.value))
                )
        else:
            i += 1

    return group_cols


def process_criteria(criteria: list[Criterion], query: Select) -> Select:
    for criterion in criteria:
        attr = col(getattr(StudyActivity, criterion.attribute.value))
        if criterion.attribute in (
            CriterionAttribute.CREATED_AT,
            CriterionAttribute.SUBMITTED_AT,
        ):
            attr = func.timezone("UTC", attr)
            attr = cast(attr, Date)

        if criterion.operator == OperatorType.EQ:
            query = query.where(attr == criterion.value)

        elif criterion.operator == OperatorType.NE:
            query = query.where(attr != criterion.value)

        elif criterion.operator == OperatorType.GT:
            query = query.where(attr > criterion.value)

        elif criterion.operator == OperatorType.GE:
            query = query.where(attr >= criterion.value)

        elif criterion.operator == OperatorType.LT:
            query = query.where(attr < criterion.value)

        elif criterion.operator == OperatorType.LE:
            query = query.where(attr <= criterion.value)

    return query


async def get_study_progress(
    user: User,
    session: AsyncSession,
    criteria: list[Criterion],
    target: AggregateTarget,
) -> list[tuple]:

    group_cols = process_group_bys(criteria)

    if target == AggregateTarget.COUNT_ITEM:
        query = (
            select(
                func.count(col(ExerciseItem.id)) + func.count(col(ReviewItem.id)),
                *group_cols,
            )
            .select_from(StudyActivity)
            .outerjoin(
                ExerciseItem,
                and_(
                    ExerciseItem.study_activity_id == StudyActivity.id,
                    or_(
                        ExerciseItem.is_deleted == False,
                        StudyActivity.is_submitted == True,
                    ),
                ),
            )
            .outerjoin(ReviewItem)
            .where(
                or_(
                    StudyActivity.is_deleted == False,
                    StudyActivity.activity_type == StudyActivityType.REVIEW,
                    StudyActivity.is_submitted == True,
                ),
            )
            .group_by(*group_cols)
        )
    elif target == AggregateTarget.COUNT_ACTIVITY:
        query = (
            select(func.count(col(StudyActivity.id)), *group_cols)
            .where(
                or_(
                    StudyActivity.is_deleted == False,
                    StudyActivity.activity_type == StudyActivityType.REVIEW,
                    StudyActivity.is_submitted == True,
                )
            )
            .group_by(*group_cols)
        )

    else:
        query = (
            select(
                func.sum(ExerciseItem.user_score),
                func.sum(ExerciseItem.max_score),
                *group_cols,
            )
            .select_from(StudyActivity)
            .join(ExerciseItem)
            .where(
                StudyActivity.activity_type == StudyActivityType.EXERCISE,
                StudyActivity.is_submitted == True,
            )
            .group_by(*group_cols)
        )
    query = query.join(Interaction).where(Interaction.user_id == user.id)
    query = process_criteria(criteria, query)

    result = (await session.execute(query)).all()
    result = [tuple(row) for row in result]

    return result


async def read_latest_study_assessment(
    user: User, session: AsyncSession
) -> StudyAssessment | None:
    query = (
        select(StudyAssessment)
        .where(StudyAssessment.user_id == user.id)
        .order_by(col(StudyAssessment.assessment_of).desc())
        .limit(1)
    )
    result = (await session.execute(query)).scalars().first()
    return result


async def read_study_assessment_by_date(
    user: User, session: AsyncSession, specific_date: date
) -> StudyAssessment:
    query = select(StudyAssessment).where(
        StudyAssessment.user_id == user.id,
        StudyAssessment.assessment_of == specific_date,
    )
    result = (await session.execute(query)).scalars().first()

    if result is None:
        raise ExceptionNotFound_404(
            "StudyAssessment",
            {
                "user_id": user.id,
                "assessment_of": str(specific_date),
            },
        )

    return result


async def read_study_assessments(
    user: User, session: AsyncSession, offset: int | None, limit: int | None
) -> list[StudyAssessment]:
    query = (
        select(StudyAssessment)
        .where(StudyAssessment.user_id == user.id)
        .order_by(col(StudyAssessment.assessment_of).desc())
    )
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)

    result = (await session.execute(query)).scalars().all()
    return list(result)
