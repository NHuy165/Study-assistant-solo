from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, func, select
from sqlmodel.sql.expression import Select

from backend.src.core.dependencies import Interaction, User
from backend.src.models_schema.activity.exercise_item import ExerciseItem
from backend.src.models_schema.activity.study_activity import StudyActivity
from backend.src.models_schema.miscellaneous.enums import (
    AggregateTarget,
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
            group_cols.append(col(getattr(StudyActivity, criterion.attribute.value)))
        else:
            i += 1

    return group_cols


def process_criteria(criteria: list[Criterion], query: Select) -> Select:
    for criterion in criteria:
        attr = getattr(StudyActivity, criterion.attribute.value)

        if criterion.operator == OperatorType.EQ:
            query = query.where(col(attr) == criterion.value)

        elif criterion.operator == OperatorType.NE:
            query = query.where(col(attr) != criterion.value)

        elif criterion.operator == OperatorType.GT:
            query = query.where(col(attr) > criterion.value)

        elif criterion.operator == OperatorType.GE:
            query = query.where(col(attr) >= criterion.value)

        elif criterion.operator == OperatorType.LT:
            query = query.where(col(attr) < criterion.value)

        elif criterion.operator == OperatorType.LE:
            query = query.where(col(attr) <= criterion.value)

    return query


async def get_study_progress(
    user: User,
    session: AsyncSession,
    criteria: list[Criterion],
    target: AggregateTarget,
) -> list[tuple]:

    group_cols = process_group_bys(criteria)
    if target == AggregateTarget.COUNT:
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
