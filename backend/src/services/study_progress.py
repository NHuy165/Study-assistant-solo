from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Date, cast, col, func, select
from sqlmodel.sql.expression import Select

from backend.src.core.dependencies import Interaction, User
from backend.src.models_schema.activity.exercise_item import ExerciseItem
from backend.src.models_schema.activity.review_item import ReviewItem
from backend.src.models_schema.activity.study_activity import StudyActivity
from backend.src.models_schema.miscellaneous.enums import (
    AggregateTarget,
    CriterionAttribute,
    OperatorType,
    StudyActivityType,
)
from backend.src.models_schema.study_progress import Criterion


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
            .outerjoin(ExerciseItem)
            .outerjoin(ReviewItem)
            .group_by(*group_cols)
        )
    elif target == AggregateTarget.COUNT_ACTIVITY:
        query = select(func.count(col(StudyActivity.id)), *group_cols).group_by(
            *group_cols
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
                StudyActivity.is_submitted,
            )
            .group_by(*group_cols)
        )
    query = query.join(Interaction).where(Interaction.user_id == user.id)
    query = process_criteria(criteria, query)

    result = (await session.execute(query)).all()
    result = [tuple(row) for row in result]

    return result
