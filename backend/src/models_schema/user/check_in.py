from datetime import date
from typing import TYPE_CHECKING, Annotated

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

if TYPE_CHECKING:
    from backend.src.models_schema.user.user import User

# ----- BASE ----- #


class CheckInBase(SQLModel):
    time: date


# ----- OUTPUT ----- #


class CheckInOutput(CheckInBase):
    pass


# ----- TABLE MODEL ----- #


class CheckIn(CheckInBase, table=True):
    __tablename__ = "check_in"  # type: ignore

    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None
    user_id: Annotated[int | None, Field(foreign_key="user.id", nullable=False)] = None

    user: "User" = Relationship(back_populates="check_ins")
