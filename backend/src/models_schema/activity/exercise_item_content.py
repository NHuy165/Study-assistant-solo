from typing import TYPE_CHECKING, Annotated

from sqlmodel import Field, Relationship, SQLModel

from backend.src.models_schema.miscellaneous.enums import ExerciseItemContentType

if TYPE_CHECKING:
    from backend.src.models_schema.activity.exercise_item import ExerciseItem

# ----- BASE ----- #


class ExerciseItemContentBase(SQLModel):
    content: str
    type: ExerciseItemContentType


# ----- OUTPUT ----- #


class ExerciseItemContentOutput(ExerciseItemContentBase):
    id: int


class ExerciseItemContentOutputAnswer(ExerciseItemContentOutput):
    is_correct: bool


# ----- TABLE MODEL ----- #


class ExerciseItemContent(ExerciseItemContentBase, table=True):
    __tablename__ = "exercise_item_content"  # type: ignore

    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None
    exercise_item_id: Annotated[
        int | None,
        Field(foreign_key="exercise_item.id", nullable=False, ondelete="CASCADE"),
    ] = None

    is_correct: bool

    exercise_item: "ExerciseItem" = Relationship(back_populates="contents")
