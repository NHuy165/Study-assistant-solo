from typing import TYPE_CHECKING, Annotated, Optional

from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship, SQLModel

from backend.src.models_schema.enums import ExerciseActivityType

if TYPE_CHECKING:
    from backend.src.models_schema.activity.study_activity import StudyActivity


# ----- BASE ----- #


class ExerciseActivityBase(SQLModel):
    exercise_activity_type: ExerciseActivityType


# ----- INPUT ----- #


class ExerciseActivityInput(ExerciseActivityBase):
    pass


# ----- TABLE MODEL ----- #


class ExerciseActivity(ExerciseActivityBase, table=True):
    __tablename__ = "exercise_activity"  # type: ignore

    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None
    study_activity_id: Annotated[
        int | None,
        Field(foreign_key="study_activity.id", nullable=False, ondelete="CASCADE"),
    ] = None

    questions: list = Field(sa_column=Column(JSON))
    size: int
    answers: list | None = Field(default=None, sa_column=Column(JSON))
    score: Annotated[float | None, Field(ge=0, le=100)] = None

    study_activity: "StudyActivity" = Relationship(back_populates="exercise_activity")
