from datetime import datetime, timezone
from typing import TYPE_CHECKING, Annotated

from pydantic import BeforeValidator, EmailStr
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from backend.src.models_schema.miscellaneous.utils import beva_forbid_none

if TYPE_CHECKING:
    from backend.src.models_schema.interaction import Interaction

# ----- BASE ----- #


class UserBase(SQLModel):
    username: Annotated[str, Field(min_length=1)]
    email: EmailStr


# ----- INPUT ----- #


class UserInput(UserBase):
    password: Annotated[str, Field(min_length=1)]


# ----- OUTPUT ----- #


class UserOutput(UserBase):
    id: int
    created_at: datetime


# ----- UPDATE ----- #


class UserUpdate(UserBase):
    username: Annotated[
        str | None, BeforeValidator(beva_forbid_none), Field(min_length=1)
    ] = None
    email: Annotated[EmailStr | None, BeforeValidator(beva_forbid_none)] = None


class UserPasswordChange(SQLModel):
    old_password: str
    new_password: str


# ----- TABLE MODEL ----- #


class User(UserBase, table=True):
    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None

    hashed_password: str

    created_at: Annotated[
        datetime,
        Field(
            sa_column=Column(DateTime(timezone=True)),
            default_factory=lambda: datetime.now(timezone.utc),
        ),
    ]

    interactions: list["Interaction"] = Relationship(back_populates="user")
