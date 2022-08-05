from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, String, Column

__all__ = ("User",)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True), nullable=False)
    email: str = Field(sa_column=Column("email", String, unique=True), nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)


# alembic revision --autogenerate -m "Created User table"