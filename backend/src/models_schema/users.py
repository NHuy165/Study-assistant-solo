from datetime import datetime, timezone
from typing import Annotated

from pydantic import EmailStr
from sqlmodel import Column, DateTime, Field, SQLModel


class UserBase(SQLModel):
    username: Annotated[str, Field(min_length=1)]
    email: EmailStr


class UserInput(UserBase):
    password: Annotated[str, Field(min_length=1)]


class UserOutput(UserBase):
    id: int
    created_at: datetime


class User(UserBase, table=True):
    id: Annotated[int | None, Field(primary_key=True, nullable=False)] = None

    hashed_password: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )

    # deleted_at: Annotated[datetime, Field(sa_column=Column(DateTime(timezone=True)))]
