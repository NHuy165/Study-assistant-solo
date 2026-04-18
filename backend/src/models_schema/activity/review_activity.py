from typing import TYPE_CHECKING, Annotated

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel

from backend.src.models_schema.enums import ReviewActivityType

if TYPE_CHECKING:
    from backend.src.models_schema.activity.study_activity import StudyActivity


# ----- BASE ----- #


class ReviewActivityBase(SQLModel):
    review_activity_type: ReviewActivityType


# ----- INPUT ----- #


class ReviewActivityInput(ReviewActivityBase):
    pass


# ----- TABLE MODEL ----- #


class ReviewActivity(ReviewActivityBase, table=True):
    __tablename__ = "review_activity"  # type: ignore

    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None
    study_activity_id: Annotated[
        int | None,
        Field(foreign_key="study_activity.id", nullable=False, ondelete="CASCADE"),
    ] = None

    contents: list = Field(sa_column=Column(JSONB))
    size: int

    study_activity: "StudyActivity" = Relationship(back_populates="review_activity")
