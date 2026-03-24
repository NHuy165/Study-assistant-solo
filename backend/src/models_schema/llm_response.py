from datetime import datetime, timezone
from typing import TYPE_CHECKING, Annotated

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.src.models_schema.interaction import Interaction

# ----- BASE ----- #


class LLMResponseBase(SQLModel):
    content: str


# ----- INPUT ----- #


class LLMResponseInput(LLMResponseBase):
    pass


# ----- OUTPUT ----- #


class LLMResponseOutput(LLMResponseBase):
    id: int
    created_at: datetime


# ----- TABLE MODEL ----- #


class LLMResponse(LLMResponseBase, table=True):
    __tablename__ = "llm_response"  # type: ignore

    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None
    interaction_id: Annotated[
        int | None,
        Field(foreign_key="interaction.id", nullable=False, ondelete="CASCADE"),
    ] = None

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    # type: flashcard, quiz...

    interaction: "Interaction" = Relationship(back_populates="llm_responses")
