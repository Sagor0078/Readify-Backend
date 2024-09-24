

import datetime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False
        )
    )

    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime.datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.datetime.now))
    updated_at: datetime.datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.datetime.now))

    def __repr__(self) -> str:
        return f"<Book {self.title}>"